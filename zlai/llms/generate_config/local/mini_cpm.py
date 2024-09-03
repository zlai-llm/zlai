from typing import Optional
from pydantic import Field
from zlai.llms.generate_config.base import GenerateConfig
from zlai.types.generate_config.completion.mini_cpm import *


__all__ = [
    "MiniCPMV26GenerateConfig"
]


class MiniCPMV26GenerateConfig(MiniCPMV26GenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="MiniCPM-V-2_6", description="模型名称")
    stream: Optional[bool] = False
