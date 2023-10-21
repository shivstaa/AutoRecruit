from typing import List, Dict, AsyncGenerator
from modal import method
import openai

from .common import stub


@stub.cls()
class ChatGPT:
    @method()
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        async for response in openai.ChatCompletion.create(messages=messages, stream=True, **kwargs):
            content = response["choices"][0].get("message", {}).get("content")
            if content:
                yield content


@stub.local_entrypoint()
def main(messages: List[Dict[str, str]], **kwargs):
    chatgpt = ChatGPT()
    for part in chatgpt.generate.call(messages, **kwargs):
        print(part, end="", flush=True)
