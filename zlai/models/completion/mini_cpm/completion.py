from typing import List, Dict, Union, Optional, Generator
from zlai.types.messages import TypeMessage
from ..glm4.utils import ProcessMessages
from ...utils import trans_messages
from ...types import TypeInferenceGenerateConfig


__all__ = [
    "mini_cpm_messages_process",
    "completion_mini_cpm",
    "stream_completion_mini_cpm",
]


def mini_cpm_messages_process(
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


def completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        generate_config: Optional[TypeInferenceGenerateConfig] = None,
) -> str:
    """

    :param model:
    :param tokenizer:
    :param messages:
    :param validate:
    :param tools:
    :param tool_choice:
    :param generate_config:
    :return:

    image = Image.open('xx.jpg').convert('RGB')
    question = 'What is in the image?'
    msgs = [{'role': 'user', 'content': [image, question]}]
    """
    messages = mini_cpm_messages_process(messages, validate, tools, tool_choice)
    content = model.chat(image=None,msgs=messages,tokenizer=tokenizer)
    return content


def stream_completion_mini_cpm(
        model,
        tokenizer,
        messages: List[TypeMessage],
        validate: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[dict, str]] = "none",
        generate_config: Optional[TypeInferenceGenerateConfig] = None,
) -> Generator[str]:
    """"""
    messages = mini_cpm_messages_process(messages, validate, tools, tool_choice)
    completion = model.chat(image=None, msgs=messages, tokenizer=tokenizer, sampling=True, stream=True)
    for chunk_content in completion:
        yield chunk_content
