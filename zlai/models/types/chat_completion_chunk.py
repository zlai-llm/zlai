import time
import json
import asyncio
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDelta, Choice


__all__ = [
    "_resp_async_generator",
]


def _get_chunk(_id: int, choice: Choice) -> ChatCompletionChunk:
    """"""
    chunk = ChatCompletionChunk(
        id=str(_id), object="chat.completion.chunk", created=int(time.time()),
        model="blah", choices=[choice],
    )
    return chunk


async def _resp_async_generator(text_resp: str):
    tokens = text_resp.split(" ")
    for i, token in enumerate(tokens):
        choice = Choice(index=0, finish_reason=None, delta=ChoiceDelta(content=token + " "))
        chunk = _get_chunk(i, choice)
        yield f"data: {json.dumps(chunk.model_dump())}\n\n"

    choice = Choice(index=0, finish_reason="stop", delta=ChoiceDelta(content=""))
    chunk = _get_chunk(i + 1, choice)
    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
