import base64
import json
from typing import AsyncGenerator

from modal import method, Image, Secret

from .common import stub


@stub.cls(
    image=Image.debian_slim().pip_install("websockets"),
    secret=Secret.from_name("my-elevenlabs-secret"),
)
class ElevenLabsTTS:
    @method()
    async def speak(self, text: str, voice_id: str) -> AsyncGenerator[str, None]:
        import websockets
        uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_monolingual_v1"
        
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({   
                "text": " ",
                "voice_settings": {"stability": 0.5, "similarity_boost": True},
                "xi_api_key": self.secret.get_secret_value()["api_key"],
            }))
            
            try:
                await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))
                await websocket.send(json.dumps({"text": ""}))
                
                async for message in websocket:
                    data = json.loads(message)
                    audio = data.get("audio")
                    is_final = data.get('isFinal')

                    if audio:
                        yield base64.b64encode(base64.b64decode(audio)).decode("utf-8")
                    elif is_final:
                        break
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
