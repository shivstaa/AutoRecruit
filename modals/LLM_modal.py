from typing import List, Dict
from modal import Image, Secret, Stub, web_endpoint
import openai
from fastapi.responses import StreamingResponse

# Configure the Modal application with necessary dependencies and secrets.
image = Image.debian_slim().pip_install("openai")
stub = Stub(
    name="hackharvard-chatgpt-stream",
    image=image,
    secrets=[Secret.from_name("my-openai-secret")],
)

@stub.function()
def stream_chat(messages: List[Dict[str, str]], **kwargs):
    """
    A generator function to stream responses from ChatGPT API.
    """
    for chunk in openai.ChatCompletion.create(messages=messages, stream=True, **kwargs):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content:
            yield content

@stub.function()
@web_endpoint()
def web(messages: List[Dict[str, str]], **kwargs):
    """
    A web endpoint to expose the streaming chat functionality.
    """
    return StreamingResponse(stream_chat(messages, **kwargs), media_type="text/html")

@stub.local_entrypoint()
def main(messages: List[Dict[str, str]], **kwargs):
    """
    Local entry point to test streaming chat functionality.
    """
    for part in stream_chat(messages, **kwargs):
        print(part, end="")
