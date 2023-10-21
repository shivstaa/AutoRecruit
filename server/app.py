import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from modal import asgi_app

from modal.common import stub
from modal.stt import Whisper
from modal.tts import ElevenLabsTTS


static_path = Path(__file__).with_name("frontend").resolve()
PUNCTUATION = [".", "?", "!", ":", ";", "*"]


@asgi_app()
def web():
    web_app = FastAPI()
    transcriber = Whisper()
    tts = ElevenLabsTTS()

    @web_app.post("/transcribe")
    async def transcribe(request: Request):
        body = await request.json()
        audio_data = body.get("audio_data")
        if audio_data is None:
            return JSONResponse(content={"error": "audio_data is required"}, status_code=400)

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
                return {
                    "type": "audio",
                    "value": tts.speak.call(sentence, "default_voice_id").object_id,
                }
            else:
                return {
                    "type": "sentence",
                    "value": sentence,
                }

        def gen():
            sentence = ""
            for segment in stub.stream_chat.call(body["input"], body["history"]).result():
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

    web_app.mount("/", StaticFiles(directory=static_path, html=True))
    return web_app
