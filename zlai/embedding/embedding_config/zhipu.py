from typing import Union, Optional
from pydantic import Field
from .base import *


__all__ = [
    "TypeZhipuEmbedding",
    "ZhipuEmbeddingConfig",
]


class ZhipuEmbeddingConfig(EmbeddingConfig):
    """"""
    model: Optional[str] = Field(default="embedding-2", description="模型名称")
    max_len: int = Field(default=512, description="最大长度")


TypeZhipuEmbedding = Union[ZhipuEmbeddingConfig]
