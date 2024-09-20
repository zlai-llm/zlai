import re
from typing import Any, Dict, List, Tuple, Union, Iterable, Optional
from threading import Thread
from pathlib import Path
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage, AudioMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.qwen2 import Qwen2GenerateConfig


__all__ = [
    "completion_qwen2_5",
    "stream_completion_qwen2_5",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = [message.to_dict() for message in messages]
    return _messages


def completion_qwen2_5(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """

    :param model:
    :param tokenizer:
    :param messages:
    :param generate_config:
    :param tools:
    :param tool_choice:
    :param kwargs:
    :return:
    """
    messages = trans_messages(messages=messages)
    text = tokenizer.apply_chat_template(
        messages, tools=tools, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**inputs, **generate_config.gen_kwargs())
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
    ]
    content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    if tools is not None:
        content = re.sub(r"<tool_call>\n|\n</tool_call>", "", content)
    completion_tokens = len(generated_ids[0])
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_qwen2_5(
        model,
        tokenizer,
        messages: List[TypeMessage],
        generate_config: Optional[Qwen2GenerateConfig],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        **kwargs: Any,
) -> Iterable[Tuple[str, CompletionUsage]]:
    messages = trans_messages(messages=messages)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer.apply_chat_template(
        messages, tools=tools, add_generation_prompt=True,
        return_dict=True, return_tensors='pt',
    ).to(model.device)
    usage.prompt_tokens = inputs.input_ids.shape[1]

    gen_config = {**inputs, "streamer": streamer, **generate_config.gen_kwargs(),}
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()
    for i, content in enumerate(streamer):
        if tools is not None:
            content = re.sub(r"<tool_call>|</tool_call>", "", str(content))
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        yield content, usage
