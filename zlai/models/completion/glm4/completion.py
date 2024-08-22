import torch
from typing import Any, List, Dict, Union, Tuple, Iterable, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage, ImageMessage
from zlai.types.completion_usage import CompletionUsage
from zlai.types.generate_config.completion.glm4 import GLM4GenerateConfig
from .utils import ProcessMessages


__all__ = [
    "completion_glm_4",
    "stream_completion_glm_4",
]


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = []
    image_idx = []
    for i, message in enumerate(messages):
        if isinstance(message, ImageMessage):
            image_idx.append(i)
            _messages.append(message.to_message(_type="glm4v"))
        else:
            _messages.append(message.model_dump())
    if len(image_idx) > 1:
        for _id in image_idx[:-1]:
            _ = _messages[_id].pop("image")
    return _messages


def glm_4_messages_process(
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        **kwargs: Any,
) -> List[Dict]:
    """"""
    if validate and tools is not None and tool_choice != 'none':
        process_messages = ProcessMessages(messages, tools, tool_choice)
        messages = process_messages.to_messages()
    messages = trans_messages(messages=messages)
    return messages


def completion_glm_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        generate_config: Optional[GLM4GenerateConfig] = None,
        **kwargs: Any,
) -> Tuple[str, CompletionUsage]:
    """"""
    messages = glm_4_messages_process(messages, validate, tools, tool_choice)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, **generate_config.gen_kwargs())
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    completion_tokens = outputs.shape[1]
    prompt_tokens = inputs.get("input_ids").shape[1]
    total_tokens = completion_tokens + prompt_tokens
    usage = CompletionUsage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens, total_tokens=total_tokens)
    return content, usage


def stream_completion_glm_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        generate_config: Optional[GLM4GenerateConfig] = None,
) -> Iterable[Tuple[str, CompletionUsage]]:
    """"""
    messages = glm_4_messages_process(messages, validate, tools, tool_choice)
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    usage.prompt_tokens = inputs.get("input_ids").shape[1]
    gen_config = {**inputs, "streamer": streamer, **generate_config.gen_kwargs()}
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()

    for i, response in enumerate(streamer):
        usage.completion_tokens += 1
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        content = str(response)
        yield content, usage
