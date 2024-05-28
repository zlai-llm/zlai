from __future__ import annotations
from typing import Optional, List

import numpy as np
from pydantic import BaseModel, Field
from zhipuai.types.chat.async_chat_completion import AsyncTaskStatus
from zhipuai.types.chat.chat_completion_chunk import ChatCompletionChunk
from .messages import Message

__all__ = [
    # LLM
    "AsyncTaskStatus",
    "CompletionUsage",
    "Completion",
    "CompletionChoice",
    "CompletionMessage",
    "AsyncCompletion",
    "ChatCompletionChunk",

    # EMB
    "EmbeddingsResponded",
    "Vector",

    # Responded
    "ValidateMessagesResponded",
    "constant_completion",
]


class CompletionUsage(BaseModel):
    prompt_tokens: int = Field(default=0, description="Prompt 的 Tokens")
    completion_tokens: int = Field(default=0, description="推理完成的 Tokens")
    total_tokens: int = Field(default=0, description="Tokens 的消耗总量")


class Function(BaseModel):
    arguments: str
    name: str


class CompletionMessageToolCall(BaseModel):
    id: str
    function: Function
    type: str


class CompletionMessage(Message):
    content: Optional[str] = None
    role: str
    tool_calls: Optional[List[CompletionMessageToolCall]] = None


class CompletionChoice(BaseModel):
    index: int = Field(default=0, description="Index")
    finish_reason: str = Field(default='', description="结束原因")
    message: CompletionMessage = Field(description="模型推理的回复消息")


class AsyncCompletion(BaseModel):
    id: Optional[str] = None
    request_id: Optional[str] = None
    model: Optional[str] = None
    task_status: str
    choices: List[CompletionChoice]
    usage: CompletionUsage


class Vector(BaseModel):
    object: str = Field(default="list", description="")
    index: Optional[int] = Field(default=0, description="")
    embedding: List[float] = Field(default=[], description="")


class EmbeddingsResponded(BaseModel):
    object: str = Field(default="list", description="")
    data: List[Vector] = Field(default=[], description="")
    model: str = Field(default="embedding-2", description="")
    usage: CompletionUsage = Field(default=CompletionUsage(), description="")

    def to_numpy(self) -> np.ndarray:
        """"""
        vectors = [vec.embedding for vec in self.data]
        return np.array(vectors)

    def to_list(self) -> List[List[float]]:
        vectors = [vec.embedding for vec in self.data]
        return vectors


class ValidateMessagesResponded(BaseModel):
    """"""
    message: str = "Success"
    access: bool = True


class Completion(BaseModel):
    model: Optional[str] = Field(default=None, description="模型名称")
    created: Optional[int] = Field(default=None, description="创建方式")
    choices: List[CompletionChoice] = Field(default=[], description="推理结果")
    request_id: Optional[str] = Field(default=None, description="请求 ID")
    id: Optional[str] = Field(default=None, description="任务 ID")
    usage: CompletionUsage = Field(default=CompletionUsage(), description="Tokens 消耗情况")


def constant_completion(
        content: Optional[str],
        role: Optional[str] = "assistant",
) -> Completion:
    """"""
    completion_message = CompletionMessage(role=role, content=content)
    completion_choice = CompletionChoice(message=completion_message, index=0, finish_reason='')
    completion = Completion(choices=[completion_choice])
    return completion
