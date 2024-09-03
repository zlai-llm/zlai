from typing import Optional
from pydantic import Field
from zlai.llms.generate_config.base import GenerateConfig
from zlai.types.generate_config.completion.glm4 import *


__all__ = [
    "GLM4GenerateConfig",
    "GLM4Chat9BGenerateConfig",
    "GLM4Chat9B1MGenerateConfig",
    "GLM4V9BGenerateConfig",
    "GLM4LongWriter9B",
    "Llama3LongWriter8B",
]


class GLM4GenerateConfig(GLM4GenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    stream: Optional[bool] = False


class GLM4Chat9BGenerateConfig(GLM4Chat9BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="glm-4-9b-chat", description="模型名称")
    stream: Optional[bool] = False


class GLM4Chat9B1MGenerateConfig(GLM4Chat9B1MGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="glm-4-9b-chat-1m", description="模型名称")
    stream: Optional[bool] = False


class GLM4V9BGenerateConfig(GLM4V9BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="glm-4v-9b", description="模型名称")
    stream: Optional[bool] = False


class GLM4LongWriter9B(GLM4LongWriter9B, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="LongWriter-glm4-9b", description="模型名称")
    stream: Optional[bool] = False


class Llama3LongWriter8B(Llama3LongWriter8B, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="LongWriter-llama3.1-8b", description="模型名称")
    stream: Optional[bool] = False
