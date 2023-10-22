from modal import method, Image, Secret

from .common import stub


@stub.cls(
    image=Image.debian_slim().pip_install(["elevenlabs", "mvt"]),
    secret=Secret.from_name("my-elevenlabs-secret"),
)
class ElevenLabsTTS:
    def __init__(self, voice_id: str, model: str = "eleven_monolingual_v1"):
        self.voice_id = voice_id
        self.model = model

    @method()
    def speak(self, text: str, voice_id: str = None):
        from elevenlabs import generate, play

        for sentence in text.split("."):
            audio = generate(
                text=sentence,
                voice=voice_id or self.voice_id,
                model=self.model,
            )

            play(audio)

    def stream_speak(self, text: str, voice_id: str = None):
        from elevenlabs import generate, stream

        for sentence in text.split("."):
            audio = generate(
                text=sentence,
                voice=voice_id or self.voice_id,
                model=self.model,
            )

            stream(audio)
