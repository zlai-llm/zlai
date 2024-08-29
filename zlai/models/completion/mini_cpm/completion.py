from typing import List, Dict, Tuple, Optional, Iterable
from zlai.types.messages import *
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.mini_cpm import MiniCPMV26GenerateConfig


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
        generate_config: Optional[MiniCPMV26GenerateConfig],
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

    kwargs = {**generate_config.model_dump()}
    messages = mini_cpm_messages_process(messages)
    content = model.chat(image=None, msgs=messages, tokenizer=tokenizer, **kwargs)

    usage.completion_tokens = len(content)
    usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
    return content, usage


def stream_completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[MiniCPMV26GenerateConfig],
        **kwargs,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    messages = mini_cpm_messages_process(messages)
    kwargs = {**generate_config.model_dump()}
    completion = model.chat(image=None, msgs=messages, tokenizer=tokenizer, sampling=True, stream=True, **kwargs)
    for chunk_content in completion:
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield chunk_content, usage
