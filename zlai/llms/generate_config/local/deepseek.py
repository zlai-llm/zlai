from typing import Optional
from pydantic import Field
from zlai.llms.generate_config.base import GenerateConfig
from zlai.types.generate_config.completion.deepseek import *


__all__ = [
    "DeepSeekGenerateConfig",
    "DeepSeekV2LiteChatGenerateConfig",
    "DeepSeekCoderV2LiteInstructChatGenerateConfig",
]


class DeepSeekGenerateConfig(DeepSeekGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    stream: Optional[bool] = False


class DeepSeekV2LiteChatGenerateConfig(DeepSeekV2LiteChatGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="DeepSeek-V2-Lite-Chat", description="模型名称")
    stream: Optional[bool] = False


class DeepSeekCoderV2LiteInstructChatGenerateConfig(DeepSeekCoderV2LiteInstructChatGenerateConfig, GenerateConfig):
    """"""
    model: Optional[str] = Field(default="DeepSeek-Coder-V2-Lite-Instruct", description="模型名称")
    stream: Optional[bool] = False
