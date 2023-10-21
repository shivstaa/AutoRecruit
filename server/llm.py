from typing import List, Dict, AsyncGenerator
from modal import method, Image, Secret

from .common import stub


@stub.cls(
    image=Image.debian_slim().pip_install(["openai"]),
    secret=Secret.from_name("my-openai-secret"),
)
class ChatGPT:
    @method()
    def generate_text(self, messages: List[Dict[str, str]], model, **kwargs):
        import openai

        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )["choices"][0]["message"]["content"]