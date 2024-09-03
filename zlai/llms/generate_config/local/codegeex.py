from typing import Optional
from pydantic import Field
from zlai.llms.generate_config.base import GenerateConfig
from zlai.types.generate_config.completion.codegeex import *


__all__ = [
    "CodeGeexGenerateConfig",
    "CodeGeex4All9BGenerateConfig",
    "CodeGeex4All9BGGUFGenerateConfig",
]


class CodeGeexGenerateConfig(CodeGeexGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    stream: Optional[bool] = False


class CodeGeex4All9BGenerateConfig(CodeGeex4All9BGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="codegeex4-all-9b", description="模型名称")
    stream: Optional[bool] = False


class CodeGeex4All9BGGUFGenerateConfig(CodeGeex4All9BGGUFGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    stream: Optional[bool] = False
