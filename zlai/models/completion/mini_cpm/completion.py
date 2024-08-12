from typing import List, Dict, Tuple, Iterable
from zlai.types.messages import *
from zlai.types.completion_usage import CompletionUsage


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
) -> Tuple[str, CompletionUsage]:
    """"""
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    for message in messages:
        if isinstance(message.content, str):
            usage.prompt_tokens += len(message.content)
        elif isinstance(message.content, list):
            for content in message.content:
                if isinstance(content, str):
                    usage.prompt_tokens += len(content)

    messages = mini_cpm_messages_process(messages)
    content = model.chat(image=None, msgs=messages, tokenizer=tokenizer)

    usage.completion_tokens = len(content)
    usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
    return content, usage


def stream_completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        **kwargs,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    messages = mini_cpm_messages_process(messages)
    completion = model.chat(image=None, msgs=messages, tokenizer=tokenizer, sampling=True, stream=True)
    for chunk_content in completion:
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield chunk_content, usage
