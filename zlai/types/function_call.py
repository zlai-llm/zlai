from typing import Dict, Union, Literal, Optional
from pydantic import BaseModel


__all__ = [
    "Function",
    "FunctionCall",
    "ChatCompletionMessageToolCall",
    "ChoiceDeltaToolCallFunction",
]


class FunctionCall(BaseModel):
    arguments: Optional[Union[str, Dict]] = None
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: str
    """The name of the function to call."""


class Function(BaseModel):
    arguments: Optional[Union[str, Dict]] = None
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: str
    """The name of the function to call."""


class ChatCompletionMessageToolCall(BaseModel):
    id: str
    """The ID of the tool call."""

    function: Function
    """The function that the model called."""

    type: Literal["function"]
    """The type of the tool. Currently, only `function` is supported."""


class ChoiceDeltaToolCallFunction(BaseModel):
    name: Optional[str] = None
    arguments: Optional[Union[str, Dict]] = None
