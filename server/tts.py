from modal import method, Image, Secret

from .common import stub


@stub.cls(
    image=Image.debian_slim().pip_install("elevenlabs"),
    secret=Secret.from_name("my-elevenlabs-secret"),
)
class ElevenLabsTTS:
    @method()
    def speak(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        from elevenlabs import generate, stream

        for sentence in text.split("."):
            audio = generate(
                text=text,
                voice=voice_id,
                model='eleven_monolingual_v1',
            )

            stream(audio)
