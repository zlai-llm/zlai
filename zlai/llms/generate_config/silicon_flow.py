from pydantic import Field
from typing import Optional, Union
from .openai import *

__all__ = [
    "TypeSiliconFlowGenerate",
    "Qwen2Instruct7BGenerateConfig",
    "Qwen2Instruct15BGenerateConfig",
    "Qwen15Chat7BGenerateConfig",
    "GLM4Chat9BGenerateConfig",
    "GLM3Chat6BGenerateConfig",
    "Yi15Chat9BGenerateConfig",
    "Yi15Chat6BGenerateConfig",
]


class Qwen2Instruct7BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-7B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-7B-Instruct", description="模型名称")


class Qwen2Instruct15BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-1.5B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-1.5B-Instruct", description="模型名称")


class Qwen15Chat7BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen1.5-7B-Chat (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen1.5-7B-Chat", description="模型名称")


class GLM4Chat9BGenerateConfig(OpenAIGenerateConfig):
    """ THUDM/glm-4-9b-chat (32K) """
    model: Optional[str] = Field(default="THUDM/glm-4-9b-chat", description="模型名称")


class GLM3Chat6BGenerateConfig(OpenAIGenerateConfig):
    """ THUDM/chatglm3-6b (32K) """
    model: Optional[str] = Field(default="THUDM/chatglm3-6b", description="模型名称")


class Yi15Chat9BGenerateConfig(OpenAIGenerateConfig):
    """ 01-ai/Yi-1.5-9B-Chat-16K (16K) """
    model: Optional[str] = Field(default="01-ai/Yi-1.5-9B-Chat-16K", description="模型名称")


class Yi15Chat6BGenerateConfig(OpenAIGenerateConfig):
    """ 01-ai/Yi-1.5-6B-Chat (4K) """
    model: Optional[str] = Field(default="01-ai/Yi-1.5-6B-Chat", description="模型名称")


TypeSiliconFlowGenerate = Union[
    Qwen2Instruct7BGenerateConfig,
    Qwen2Instruct15BGenerateConfig,
    Qwen15Chat7BGenerateConfig,
    GLM4Chat9BGenerateConfig,
    GLM3Chat6BGenerateConfig,
    Yi15Chat9BGenerateConfig,
    Yi15Chat6BGenerateConfig,
]
