from typing import List, AsyncGenerator
from modal import Image, Secret, Stub, web_endpoint
from fastapi.responses import StreamingResponse
import asyncio
import websockets
import json
import base64

# Configure the Modal application with necessary dependencies and secrets.
image = Image.debian_slim().pip_install(["openai", "websockets", "httpx"])
stub = Stub(
    name="stt-stream",
    image=image,
    secrets=[Secret.from_name("my-stt-secret")],
)

async def speech_to_text_input_streaming(
    audio_iterator: AsyncGenerator[bytes, None], stt_api_key: str
) -> AsyncGenerator[str, None]:
    # TODO: Connect to STT API (update URL accordingly)
    uri = f"wss://api.stt.io/stream"

    async with websockets.connect(uri) as websocket:
        # Send initialization message if required
        await websocket.send(json.dumps({"api_key": stt_api_key}))

        # Send audio data
        async for audio_chunk in audio_iterator:
            await websocket.send(audio_chunk)

        # Indicate end of stream
        await websocket.send(b"")

        # Receive and yield transcribed text
        async for message in websocket:
            data = json.loads(message)
            transcript = data.get("transcript")
            if transcript:
                yield transcript

@stub.function()
async def stt_stream(audio: List[bytes]) -> AsyncGenerator[str, None]:
    stt_api_key = stub.secrets["my-stt-secret"].get_secret_value()["api_key"]
    async def audio_iterator():
        for chunk in audio:
            yield chunk

    text_stream = speech_to_text_input_streaming(audio_iterator(), stt_api_key)
    async for chunk in text_stream:
        yield chunk

@stub.function()
@web_endpoint()
async def web(audio: List[bytes]) -> StreamingResponse:
    return StreamingResponse(stt_stream(audio), media_type="text/html")

@stub.local_entrypoint()
def main(audio: List[bytes]):
    asyncio.run(stt_stream(audio))
