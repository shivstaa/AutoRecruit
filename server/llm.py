from typing import List, Dict, AsyncGenerator
from modal import method, Image, Secret

from .common import stub


@stub.cls(
    image=Image.debian_slim().pip_install(["openai"]),
    secret=Secret.from_name("my-openai-secret"),
)
class ChatGPT:
    @method()
    def chat(self, messages: List[Dict[str, str]], model, **kwargs):
        import openai

        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )["choices"][0]["message"]["content"]
    
    @method()
    def stream_chat(self, messages: List[Dict[str, str]], model, **kwargs) -> AsyncGenerator[str, None]:
        import openai

        for chunk in openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content is not None:
                yield content
