from typing import Optional
from pydantic import Field
from zlai.llms.generate_config.base import GenerateConfig
from zlai.types.generate_config.completion.qwen2 import *


__all__ = [
    "Qwen2GenerateConfig",
    "Qwen2Instruct05BGenerateConfig",
    "Qwen2Instruct15BGenerateConfig",
    "Qwen2Instruct7BGenerateConfig",
    "Qwen2Audio7BInstructGenerateConfig",
    "Qwen2VLInstructGenerateConfig",
    "Qwen2VL7BInstructGenerateConfig",
    "Qwen2VL2BInstructGenerateConfig",
]


class Qwen2GenerateConfig(Qwen2GenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    stream: Optional[bool] = False


class Qwen2Instruct05BGenerateConfig(Qwen2Instruct05BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-0.5B-Instruct", description="模型名称")
    stream: Optional[bool] = False


class Qwen2Instruct15BGenerateConfig(Qwen2Instruct15BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-1.5B-Instruct", description="模型名称")
    stream: Optional[bool] = False


class Qwen2Instruct7BGenerateConfig(Qwen2Instruct7BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-7B-Instruct", description="模型名称")
    stream: Optional[bool] = False


class Qwen2Audio7BInstructGenerateConfig(Qwen2Audio7BInstructGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-Audio-7B-Instruct", description="模型名称")
    stream: Optional[bool] = False


class Qwen2VLInstructGenerateConfig(Qwen2VLInstructGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="", description="模型名称")
    stream: Optional[bool] = False


class Qwen2VL2BInstructGenerateConfig(Qwen2VL2BInstructGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-VL-2B-Instruct", description="模型名称")
    stream: Optional[bool] = False


class Qwen2VL7BInstructGenerateConfig(Qwen2VL7BInstructGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen2-VL-7B-Instruct", description="模型名称")
    stream: Optional[bool] = False
