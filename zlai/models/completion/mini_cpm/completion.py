from typing import List, Dict, Iterable
from zlai.types.messages import *


__all__ = [
    "mini_cpm_messages_process",
    "completion_mini_cpm",
    "stream_completion_mini_cpm",
]


def mini_cpm_messages_process(
        messages: List[TypeMessage],
) -> List[Dict]:
    """"""
    _messages = []
    for message in messages:
        if isinstance(message, ImageMessage):
            msg = message.to_message(_type="mini_cpm")
        else:
            msg = message.model_dump()
        _messages.append(msg)
    return _messages


def completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        **kwargs,
) -> str:
    """"""
    messages = mini_cpm_messages_process(messages)
    content = model.chat(image=None, msgs=messages, tokenizer=tokenizer)
    return content


def stream_completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        **kwargs,
) -> Iterable[str]:
    """"""
    messages = mini_cpm_messages_process(messages)
    completion = model.chat(image=None, msgs=messages, tokenizer=tokenizer, sampling=True, stream=True)
    for chunk_content in completion:
        yield chunk_content
