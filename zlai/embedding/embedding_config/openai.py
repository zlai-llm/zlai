from typing import Union, Optional
from pydantic import Field
from .base import *


__all__ = [
    "TypeOpenAIEmbedding",
    "OpenAIEmbeddingConfig",
    "BGEM3EmbeddingConfig",
]


class OpenAIEmbeddingConfig(EmbeddingConfig):
    """"""
    model: Optional[str] = Field(default="bge-m3", description="模型名称")
    max_len: int = Field(default=8000, description="最大长度")


class BGEM3EmbeddingConfig(OpenAIEmbeddingConfig):
    """"""
    model: Optional[str] = Field(default="bge-m3", description="模型名称")


TypeOpenAIEmbedding = Union[
    OpenAIEmbeddingConfig,
    BGEM3EmbeddingConfig,
]
