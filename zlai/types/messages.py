from typing import List, Dict, Union, Literal, Optional
from pydantic import BaseModel, Field
from .function_call import *


__all__ = [
    "Message",
    "ChatMessage",
    "SystemMessage",
    "SystemToolsMessage",
    "UserMessage",
    "AssistantMessage",
    "AssistantWithMetadataMessage",
    "ObservationMessage",
    "FunctionMessage",
    "ToolMessage",
    "ToolsMessage",
    "ChatCompletionMessage",
    "TypeMessage",
]


class Message(BaseModel):
    """"""
    role: str = Field(default="", description="角色")
    content: str = Field(default="", description="对话内容")


class ChatMessage(Message):
    """"""
    role: str = Field(..., description="角色")
    content: str = Field(..., description="对话内容")


class SystemMessage(Message):
    """"""
    role: Literal["system"] = Field(default="system", description="角色")
    content: str = Field(..., description="对话内容")


class SystemToolsMessage(SystemMessage):
    """for glm4 function call"""
    tools: Optional[List[Dict]] = Field(default=None, description="工具列表")


class UserMessage(Message):
    """"""
    role: Literal["user"] = Field("user", description="角色")
    content: str = Field(..., description="对话内容")


class AssistantMessage(Message):
    """"""
    role: Literal["assistant"] = Field("assistant", description="角色")
    content: str = Field(..., description="对话内容")


class AssistantWithMetadataMessage(AssistantMessage):
    """for glm4 function call"""
    metadata: str = Field(default=None, description="metadata")
    content: str = Field(default="", description="对话内容")


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


class ChatCompletionMessage(BaseModel):
    """"""
    role: Literal["user", "assistant", "system", "tool"] = Field(..., description="""The role of the author of this message.""")
    content: Optional[str] = Field(default=None, description="""The contents of the message.""")
    function_call: Optional[FunctionCall] = Field(default=None, description="""
        Deprecated and replaced by `tool_calls`.
        The name and arguments of a function that should be called, as generated by the
        model.
    """)
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = Field(default=None, description="""
        The tool calls generated by the model, such as function calls.
    """)


TypeMessage = Union[
    Message,
    ChatMessage,
    SystemMessage,
    SystemToolsMessage,
    UserMessage,
    AssistantMessage,
    AssistantWithMetadataMessage,
    ObservationMessage,
    FunctionMessage,
    ToolMessage,
    ToolsMessage,
    ChatCompletionMessage,
]
