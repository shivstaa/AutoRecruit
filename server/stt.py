import tempfile
import time
from modal import method, Image, Secret

from .common import stub


MODEL_NAMES = ["base.en", "large-v2"]

transcriber_image = (
    Image.debian_slim(python_version="3.10.8")
    .apt_install("git", "ffmpeg")
    .pip_install(
        "https://github.com/openai/whisper/archive/v20230314.tar.gz",
        "ffmpeg-python",
        "openai",
    )
)


def load_audio(data: bytes, sr: int = 16000):
    import ffmpeg
    import numpy as np

    try:
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        fp.write(data)
        fp.close()
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(
                fp.name,
                threads=0,
                format="f32le",
                acodec="pcm_f32le",
                ac=1,
                ar="48k",
            )
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(
                cmd=["ffmpeg", "-nostdin"],
                capture_stdout=True,
                capture_stderr=True,
            )
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.float32).flatten()


@stub.cls(
    gpu="A10G",
    container_idle_timeout=180,
    image=transcriber_image,
    secret=Secret.from_name("my-openai-secret"),
)
class Whisper:
    def __enter__(self):
        import torch
        import whisper

        self.use_gpu = torch.cuda.is_available()
        device = "cuda" if self.use_gpu else "cpu"
        self.models = {
            model_name: whisper.load_model(model_name, device=device) for model_name in MODEL_NAMES
        }

    @method()
    async def transcribe_segment(
        self,
        audio_data: bytes,
        model_name: str = None,
        use_api: bool = False,
    ):
        import openai
        t0 = time.time()
        np_array = load_audio(audio_data)
        if use_api:
            result = openai.Audio.create(
                model="whisper-large",
                audio=np_array.tobytes(),
                language="en",
            )
        elif model_name:
            result = self.models[model_name].transcribe(np_array, language="en", fp16=self.use_gpu)  # type: ignore
        else:
            result = {"error": "No transcription model specified"}

        print(f"Transcribed in {time.time() - t0:.2f}s")

        return result
