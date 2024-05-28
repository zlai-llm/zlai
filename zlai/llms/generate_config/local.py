from pydantic import Field
from typing import Union, Optional
from ...schema.url import Model
from .base import GenerateConfig


__all__ = [
    # type
    "TypeLocalGenerate",

    # Qwen 1.5 generate config
    "Qwen15GenerateConfig",
    "Qwen15Chat7BGenerateConfig",
    "Qwen15Chat14BGenerateConfig",
    "Qwen15Chat72BAWQGenerateConfig",
    "Qwen15Chat72BInt4GenerateConfig",
    "Qwen15Chat72BInt8GenerateConfig",
    # ChatGLM 6B generate config
    "ChatGLM6BGenerateConfig",
    "ChatGLM6B128KGenerateConfig",
]

model = Model()


class Qwen15GenerateConfig(GenerateConfig):
    """"""
    repetition_penalty: float = Field(default=1.05, description="")
    max_new_tokens: int = Field(default=2048, description="")
    do_sample: bool = Field(default=True, description="")
    temperature: float = Field(default=0.7, description="")
    top_p: float = Field(default=0.8, description="")
    top_k: int = Field(default=20, description="")
    stream: bool = Field(default=False, description="")
    incremental: Optional[bool] = Field(default=False, description="默认为 False，如果设置为 True，模型仅输出增量 token")


class Qwen15Chat7BGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default=model.qwen_1_5_7b_chat, description="模型名称")


class Qwen15Chat14BGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default=model.qwen_1_5_14b_chat, description="模型名称")


class Qwen15Chat72BAWQGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default=model.qwen_1_5_72b_chat_awq, description="模型名称")


class Qwen15Chat72BInt4GenerateConfig(Qwen15GenerateConfig):
    model: Optional[str] = Field(default=model.qwen_1_5_72b_chat_init4, description="模型名称")


class Qwen15Chat72BInt8GenerateConfig(Qwen15GenerateConfig):
    model: Optional[str] = Field(default=model.qwen_1_5_72b_chat_init8, description="模型名称")


class ChatGLMGenerateConfig(GenerateConfig):
    """"""
    num_beams: int = 1
    do_sample: bool = Field(default=True, description="")
    top_p: float = Field(default=0.8, description="")
    temperature: float = Field(default=0.8, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")
    stream: bool = Field(default=False, description="")


class ChatGLM6BGenerateConfig(ChatGLMGenerateConfig):
    """
    GLMGenerateConfig
    """
    model: Optional[str] = Field(default=model.chatglm3_6b, description="模型名称")
    max_length: int = Field(default=8192, description="上下文长度")
    top_p: float = Field(default=0.8, description="")
    temperature: float = Field(default=0.8, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")


class ChatGLM6B128KGenerateConfig(ChatGLMGenerateConfig):
    """"""
    model: Optional[str] = Field(default=model.chatglm3_6b_128k, description="模型名称")
    max_length: int = Field(default=131072, description="上下文长度")
    top_p: float = Field(default=0.7, description="")
    temperature: float = Field(default=0.95, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0")


TypeLocalGenerate = Union[
    GenerateConfig,
    # Qwen 1.5
    Qwen15GenerateConfig,
    Qwen15Chat7BGenerateConfig,
    Qwen15Chat14BGenerateConfig,
    Qwen15Chat72BAWQGenerateConfig,
    Qwen15Chat72BInt4GenerateConfig,
    Qwen15Chat72BInt8GenerateConfig,
    # chatglm6b
    ChatGLM6BGenerateConfig,
    ChatGLM6B128KGenerateConfig,
]

