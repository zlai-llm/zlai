from pydantic import Field
from typing import Literal, Optional, Union
from .base import Message


__all__ = [
    "ObservationMessage",
    "FunctionMessage",
    "ToolMessage",
    "ToolsMessage",
]


class ObservationMessage(Message):
    """"""
    role: Literal["observation"] = Field("observation", description="角色")
    content: str = Field(..., description="对话内容")


class FunctionMessage(ObservationMessage):
    pass


class ToolMessage(ObservationMessage):
    """"""
    function_call: bool = Field(default=True, description="是否为工具调用")


class ToolsMessage(Message):
    """"""
    role: Literal["tool"] = Field(default="tool", description="角色")
    content: str = Field(default="", description="对话内容")
    tool_call_id: Optional[Union[int, str, dict]] = Field(default=None, description="id")
