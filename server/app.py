import json

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from modal import asgi_app, Secret, Image

from server.common import stub
from server.stt import Whisper
from server.tts import ElevenLabsTTS
from server.llm import ChatGPT


PUNCTUATION = [".", "?", "!", ":", ";", "*"]
auth_scheme = HTTPBearer()


app_image = Image.debian_slim().pip_install(["fastapi", "uvicorn", "httpx", "pydantic", "pyyaml", "pydantic-yaml"])


@stub.function(
    image=app_image,
)
@asgi_app()
def web():
    web_app = FastAPI()

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

    transcriber = Whisper()
    tts = ElevenLabsTTS()
    text_generator = ChatGPT()

    async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        auth_token_secret = Secret.from_name("my-web-auth-token")
        auth_token = auth_token_secret.get()
        if token.credentials != auth_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect bearer token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token.credentials

    @web_app.post("/transcribe")
    async def transcribe(request: Request):
        body = await request.json()
        audio_data = body.get("audio_data")
        if audio_data is None:
            return {"error": "audio_data is required"}, 400

        model_name = body.get("model_name")
        use_api = body.get("use_api", False)

        result = await transcriber.transcribe_segment.call(audio_data, model_name, use_api)
        return result["text"]

    @web_app.post("/generate")
    async def generate(request: Request):
        body = await request.json()
        tts_enabled = body.get("tts", False)

        def speak(sentence):
            if tts_enabled:
                fc = tts.speak.spawn(sentence, "default_voice_id")
                return {
                    "type": "audio",
                    "value": fc.object_id,
                }
            else:
                return {
                    "type": "sentence",
                    "value": sentence,
                }

        def gen():
            sentence = ""
            for segment in text_generator.generate_text.call(body["input"], body["history"]).result():
                yield {"type": "text", "value": segment}
                sentence += segment
                for p in PUNCTUATION:
                    if p in sentence:
                        prev_sentence, new_sentence = sentence.rsplit(p, 1)
                        yield speak(prev_sentence)
                        sentence = new_sentence

            if sentence:
                yield speak(sentence)

        def gen_serialized():
            for i in gen():
                yield json.dumps(i) + "\x1e"

        return StreamingResponse(
            gen_serialized(),
            media_type="text/event-stream",
        )

    return web_app
