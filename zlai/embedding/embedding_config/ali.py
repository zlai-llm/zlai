from typing import Union
from pydantic import Field
from .base import *


__all__ = [
    "TypeAliEmbedding",
    "AliEmbeddingV1Config",
    "AliEmbeddingAsyncV1Config",
    "AliEmbeddingV2Config",
    "AliEmbeddingAsyncV2Config",
]


class AliEmbeddingV1Config(EmbeddingConfig):
    """ 通用文本向量
    中文、英语、西班牙语、法语、葡萄牙语、印尼语。
    """
    model: str = Field(default="text-embedding-v1")
    dimension: int = Field(default=1536)
    batch_size: int = Field(default=25)
    max_len: int = Field(default=2048)


class AliEmbeddingAsyncV1Config(EmbeddingConfig):
    """ 通用文本向量
    中文、英语、西班牙语、法语、葡萄牙语、印尼语。
    """
    model: str = Field(default="text-embedding-async-v1")
    dimension: int = Field(default=1536)
    batch_size: int = Field(default=100000)
    max_len: int = Field(default=2048)


class AliEmbeddingV2Config(EmbeddingConfig):
    """ 通用文本向量
    中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语。
    """
    model: str = Field(default="text-embedding-v2")
    dimension: int = Field(default=1536)
    batch_size: int = Field(default=25)
    max_len: int = Field(default=2048)


class AliEmbeddingAsyncV2Config(EmbeddingConfig):
    """ 通用文本向量
    中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语。
    """
    model: str = Field(default="text-embedding-async-v2")
    dimension: int = Field(default=1536)
    batch_size: int = Field(default=100000)
    max_len: int = Field(default=2048)


TypeAliEmbedding = Union[
    AliEmbeddingV1Config,
    AliEmbeddingAsyncV1Config,
    AliEmbeddingV2Config,
    AliEmbeddingAsyncV2Config,
]
