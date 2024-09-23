from typing import List, Dict, Union, Literal, Optional
from pydantic import Field
from .base import Message
from .content import TextContent


__all__ = [
    "ChatMessage",
    "SystemMessage",
    "SystemToolsMessage",
    "UserMessage",
    "AssistantMessage",
    "AssistantWithMetadataMessage",
]


class ChatMessage(Message):
    """"""
    role: str = Field(..., description="角色")
    content: Optional[str] = Field(..., description="对话内容")


class SystemMessage(Message):
    """"""
    role: Literal["system"] = Field(default="system", description="角色")
    content: Optional[str] = Field(..., description="对话内容")


class SystemToolsMessage(SystemMessage):
    """for glm4 function call"""
    tools: Optional[List[Dict]] = Field(default=None, description="工具列表")


class UserMessage(Message):
    """"""
    role: Literal["user"] = Field("user", description="角色")
    content: Optional[Union[str, List[TextContent]]] = Field(..., description="对话内容")


class AssistantMessage(Message):
    """"""
    role: Literal["assistant"] = Field("assistant", description="角色")
    content: Optional[str] = Field(..., description="对话内容")


class AssistantWithMetadataMessage(AssistantMessage):
    """for glm4 function call"""
    metadata: str = Field(default=None, description="metadata")
    content: Optional[Union[str, Dict]] = Field(default="", description="对话内容")
