from pydantic import Field
from typing import Union, Optional
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeGLM3Generate",
    "ChatGLM3GenerateConfig",
    "ChatGLM36BGenerateConfig",
    "ChatGLM36B128KGenerateConfig",
]


class ChatGLM3GenerateConfig(GenerateConfig):
    """"""
    num_beams: int = 1
    do_sample: bool = Field(default=True, description="")
    top_p: float = Field(default=0.8, description="")
    temperature: float = Field(default=0.8, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")
    stream: bool = Field(default=False, description="")


class ChatGLM36BGenerateConfig(ChatGLM3GenerateConfig):
    """
    GLMGenerateConfig
    """
    model: Optional[str] = Field(default="chatglm3-6b", description="模型名称")
    max_length: int = Field(default=8192, description="上下文长度")
    top_p: float = Field(default=0.8, description="")
    temperature: float = Field(default=0.8, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")


class ChatGLM36B128KGenerateConfig(ChatGLM3GenerateConfig):
    """"""
    model: Optional[str] = Field(default="chatglm3-6b-128k", description="模型名称")
    max_length: int = Field(default=131072, description="上下文长度")
    top_p: float = Field(default=0.7, description="")
    temperature: float = Field(default=0.95, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")


TypeGLM3Generate = Union[
    ChatGLM3GenerateConfig,
    ChatGLM36BGenerateConfig,
    ChatGLM36B128KGenerateConfig,
]
