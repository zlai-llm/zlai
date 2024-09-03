from pydantic import Field
from typing import Optional, Union
from .openai import *

__all__ = [
    "TypeSiliconFlowGenerate",
    "Qwen2Instruct72BGenerateConfig",
    "Qwen2Instruct57BA14BGenerateConfig",
    "Qwen2Instruct7BGenerateConfig",
    "Qwen2Instruct15BGenerateConfig",
    "Qwen15Chat110BGenerateConfig",
    "Qwen15Chat32BGenerateConfig",
    "Qwen15Chat14BGenerateConfig",
    "Qwen15Chat7BGenerateConfig",
    "GLM4Chat9BGenerateConfig",
    "GLM3Chat6BGenerateConfig",
    "Yi15Chat9BGenerateConfig",
    "Yi15Chat6BGenerateConfig",
    "DeepSeekCoderV2InstructGenerateConfig",
    "DeepSeekV2ChatGenerateConfig",
    "DeepSeekLLM67BChatGenerateConfig",
]


class Qwen2Instruct72BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-72B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-72B-Instruct", description="模型名称")


class Qwen2Instruct57BA14BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-57B-A14B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-57B-A14B-Instruct", description="模型名称")


class Qwen2Instruct7BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-7B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-7B-Instruct", description="模型名称")


class Qwen2Instruct15BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen2-1.5B-Instruct (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen2-1.5B-Instruct", description="模型名称")


class Qwen15Chat110BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen1.5-110B-Chat (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen1.5-110B-Chat", description="模型名称")


class Qwen15Chat32BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen1.5-32B-Chat (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen1.5-32B-Chat", description="模型名称")


class Qwen15Chat14BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen1.5-14B-Chat (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen1.5-14B-Chat", description="模型名称")


class Qwen15Chat7BGenerateConfig(OpenAIGenerateConfig):
    """ Qwen/Qwen1.5-7B-Chat (32K) """
    model: Optional[str] = Field(default="Qwen/Qwen1.5-7B-Chat", description="模型名称")


class GLM4Chat9BGenerateConfig(OpenAIGenerateConfig):
    """ THUDM/glm-4-9b-chat (32K) """
    model: Optional[str] = Field(default="THUDM/glm-4-9b-chat", description="模型名称")


class GLM3Chat6BGenerateConfig(OpenAIGenerateConfig):
    """ THUDM/chatglm3-6b (32K) """
    model: Optional[str] = Field(default="THUDM/chatglm3-6b", description="模型名称")


class Yi15Chat34BGenerateConfig(OpenAIGenerateConfig):
    """ 01-ai/Yi-1.5-34B-Chat-16K (16K) """
    model: Optional[str] = Field(default="01-ai/Yi-1.5-34B-Chat-16K", description="模型名称")


class Yi15Chat9BGenerateConfig(OpenAIGenerateConfig):
    """ 01-ai/Yi-1.5-9B-Chat-16K (16K) """
    model: Optional[str] = Field(default="01-ai/Yi-1.5-9B-Chat-16K", description="模型名称")


class Yi15Chat6BGenerateConfig(OpenAIGenerateConfig):
    """ 01-ai/Yi-1.5-6B-Chat (4K) """
    model: Optional[str] = Field(default="01-ai/Yi-1.5-6B-Chat", description="模型名称")


class DeepSeekCoderV2InstructGenerateConfig(OpenAIGenerateConfig):
    """ deepseek-ai/DeepSeek-Coder-V2-Instruct (32K) """
    model: Optional[str] = Field(default="deepseek-ai/DeepSeek-Coder-V2-Instruct", description="模型名称")


class DeepSeekV2ChatGenerateConfig(OpenAIGenerateConfig):
    """ deepseek-ai/DeepSeek-V2-Chat (32K) """
    model: Optional[str] = Field(default="deepseek-ai/DeepSeek-V2-Chat", description="模型名称")


class DeepSeekLLM67BChatGenerateConfig(OpenAIGenerateConfig):
    """ deepseek-ai/deepseek-llm-67b-chat (32K) """
    model: Optional[str] = Field(default="deepseek-ai/deepseek-llm-67b-chat", description="模型名称")


TypeSiliconFlowGenerate = Union[
    Qwen2Instruct72BGenerateConfig,
    Qwen2Instruct57BA14BGenerateConfig,
    Qwen2Instruct7BGenerateConfig,
    Qwen2Instruct15BGenerateConfig,
    Qwen15Chat110BGenerateConfig,
    Qwen15Chat32BGenerateConfig,
    Qwen15Chat14BGenerateConfig,
    Qwen15Chat7BGenerateConfig,
    GLM4Chat9BGenerateConfig,
    GLM3Chat6BGenerateConfig,
    Yi15Chat9BGenerateConfig,
    Yi15Chat6BGenerateConfig,
    DeepSeekCoderV2InstructGenerateConfig,
    DeepSeekV2ChatGenerateConfig,
    DeepSeekLLM67BChatGenerateConfig,
]
