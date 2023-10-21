from typing import AsyncGenerator, List
from modal import Image, Secret, Stub, web_endpoint
from fastapi.responses import StreamingResponse
import asyncio
import websockets
import json
import base64

# Configure the Modal application with necessary dependencies and secrets.
image = Image.debian_slim().pip_install(["openai", "websockets", "httpx"])
stub = Stub(
    name="tts-stream",
    image=image,
    secrets=[Secret.from_name("my-elevenlabs-secret")],
)

async def text_to_speech_input_streaming(
    voice_id: str, text_iterator: AsyncGenerator[str, None], elevenlabs_api_key: str
) -> AsyncGenerator[bytes, None]:
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_monolingual_v1"
    
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": True},
            "xi_api_key": elevenlabs_api_key,
        }))

        try:
            async for text in text_iterator:
                await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))
            
            await websocket.send(json.dumps({"text": ""}))

            async for message in websocket:
                data = json.loads(message)
                audio = data.get("audio")
                is_final = data.get('isFinal')

                if audio:
                    yield base64.b64decode(audio)
                elif is_final:
                    break
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

async def stream(audio_stream: AsyncGenerator[bytes, None]) -> AsyncGenerator[str, None]:
    async for chunk in audio_stream:
        yield base64.b64encode(chunk).decode("utf-8")

@stub.function()
async def tts_stream(text: str, voice_id: str) -> AsyncGenerator[str, None]:
    elevenlabs_api_key = stub.secrets["my-elevenlabs-secret"].get_secret_value()["api_key"]
    async def text_iterator():
        yield text

    audio_stream = text_to_speech_input_streaming(voice_id, text_iterator(), elevenlabs_api_key)
    async for chunk in stream(audio_stream):
        yield chunk

@stub.function()
@web_endpoint()
async def web(text: str, voice_id: str) -> StreamingResponse:
    return StreamingResponse(tts_stream(text, voice_id), media_type="text/html")

@stub.local_entrypoint()
def main(text: str, voice_id: str):
    asyncio.run(tts_stream(text, voice_id))
