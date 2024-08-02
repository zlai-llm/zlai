import torch
from typing import List, Dict, Union, Optional
from threading import Thread
from transformers import TextIteratorStreamer
from zlai.types.messages import TypeMessage
from .utils import ProcessMessages
from ...utils import trans_messages
from ...types import TypeInferenceGenerateConfig


__all__ = [
    "completion_glm_4",
    "stream_completion_glm_4",
]


def glm_4_messages_process(
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
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
        generate_config: Optional[TypeInferenceGenerateConfig] = None,
) -> str:
    """"""
    messages = glm_4_messages_process(messages, validate, tools, tool_choice)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, **generate_config.gen_kwargs())
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return content


def stream_completion_glm_4(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        generate_config: Optional[TypeInferenceGenerateConfig] = None,
):
    """"""
    messages = glm_4_messages_process(messages, validate, tools, tool_choice)

    streamer = TextIteratorStreamer(tokenizer)
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    drop_tokens = tokenizer.special_tokens_map.get("additional_special_tokens")
    gen_config = {**inputs, "streamer": streamer, **generate_config.gen_kwargs()}
    thread = Thread(target=model.generate, kwargs=gen_config)
    thread.start()

    for i, response in enumerate(streamer):
        content = str(response)
        if "[gMASK]" in content and i == 0:
            drop_tokens.insert(0, content)
        for t in drop_tokens:
            content = content.replace(t, "")
        if content:
            yield content
