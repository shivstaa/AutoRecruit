import os
import base64

from fastapi import FastAPI, Request, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from modal import asgi_app, Image, Secret

from server.common import stub
from server.stt import Whisper
from server.tts import ElevenLabsTTS
from server.llm import ChatGPT


PUNCTUATION = [".", "?", "!", ":", ";", "*"]
auth_scheme = HTTPBearer()


def check_authorization(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if token.credentials != os.environ["AUTH_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.credentials


@stub.function(
    image=Image.debian_slim().pip_install(["fastapi", "uvicorn", "httpx", "pydantic", "pyyaml", "pydantic-yaml"]),
    secret=Secret.from_name("my-web-auth-token")
)
@asgi_app()
def web():
    web_app = FastAPI(dependencies=[Depends(check_authorization)])
    stt = Whisper()
    tts = ElevenLabsTTS(voice_id="21m00Tcm4TlvDq8ikWAM")
    llm = ChatGPT()

    # Configure CORS
    origins = [
        "http://localhost:3000",  # Local frontend server
        "https://yourfrontenddomain.com",  # Production frontend server
    ]
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @web_app.post("/transcribe")
    async def transcribe(request: Request):
        try:
            body = await request.json()
            audio_data = body.get("audio_data")
            if audio_data is None:
                raise HTTPException(status_code=400, detail="Missing audio_data")
            audio_data = base64.b64decode(audio_data)

            model_name = body.get("model_name")
            transcription_text = stt.transcribe_segment.remote(audio_data, model_name)
            return {"text": transcription_text}
        except Exception as e:
            # Log the error for debugging
            print(f"Error during transcription: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @web_app.post("/transcribe_file")
    async def transcribe_file(audio_data: UploadFile = File(...)):
        content = await audio_data.read()
        transcription_text = stt.transcribe_segment.remote(content, None)
        return {"text": transcription_text}

    @web_app.post("/chat")
    async def chat(request: Request):
        body = await request.json()
        messages = body.get("messages")
        model = body.get("model")

        completion = llm.chat.remote(messages, model)
        return {"text": completion}

    @web_app.post("/stream_chat")
    async def stream_chat(request: Request):
        body = await request.json()
        messages = body.get("messages")
        model = body.get("model")

        async def generate():
            async for chunk in llm.stream_chat.remote(messages, model):
                yield chunk

        return StreamingResponse(generate(), media_type="text/html")

    @web_app.post("/speak")
    async def speak(request: Request):
        try:
            body = await request.json()
            text = body.get("text")
            if text is None:
                raise HTTPException(status_code=400, detail="text is required")
            
            tts.speak.remote(text)
            
        except Exception as e:
            print(f"Error during text-to-speech: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @web_app.post("/stream_speak")
    async def stream_speak(request: Request):
        try:
            body = await request.json()
            text = body.get("text")
            if text is None:
                raise HTTPException(status_code=400, detail="text is required")
            
            tts.stream_speak.remote(text)
            
        except Exception as e:
            print(f"Error during text-to-speech: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return web_app
