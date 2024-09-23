import string
import random
from typing import Dict, List, Union, Optional
from zlai.types.function_call import Function, ChatCompletionMessageToolCall
from zlai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCallFunction, ChoiceDeltaToolCall
from zlai.types.messages import ChatCompletionMessage


__all__ = [
    "message_instance",
    "message_function_call",
    "choice_function_call",
]


def generate_id(prefix: str, k: int = 29) -> str:
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return f"{prefix}{suffix}"


def message_function_call(
        functions: Optional[List[Dict]]
) -> Optional[List[ChatCompletionMessageToolCall]]:
    """"""
    if functions is None:
        return None
    new_tool_calls = []
    for i, function in enumerate(functions):
        new_tool_calls.append(ChatCompletionMessageToolCall(
            id=generate_id('call_', 24),
            function=Function.model_validate(function),
            type="function",
        ))
    return new_tool_calls


def choice_function_call(
        functions: Optional[List[Dict]]
) -> Optional[List[ChoiceDeltaToolCall]]:
    """"""
    if functions is None:
        return None
    new_tool_calls = []
    for i, function in enumerate(functions):
        new_tool_calls.append(ChoiceDeltaToolCall(
            id=generate_id('call_', 24),
            index=i, type="function",
            function=ChoiceDeltaToolCallFunction.model_validate(function),
        ))
    return new_tool_calls


def message_instance(
        content: str,
        functions: Optional[List[Dict]] = None,
        stream: Optional[bool] = False,
) -> Union[ChatCompletionMessage, ChoiceDelta]:
    """"""
    if stream:
        tool_calls = choice_function_call(functions)
        response_message = ChoiceDelta(
            role="assistant",
            content="" if tool_calls else content,
            function_call=None,
            tool_calls=tool_calls,
        )
    else:
        tool_calls = message_function_call(functions)
        response_message = ChatCompletionMessage(
            role="assistant",
            content="" if tool_calls else content,
            function_call=None,
            tool_calls=tool_calls,
        )
    return response_message

