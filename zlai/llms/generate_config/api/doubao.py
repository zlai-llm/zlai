from pydantic import Field
from typing import Optional, Union
from .openai import OpenAIGenerateConfig


__all__ = [
    # Type
    "TypeDouBaoGenerate",
    # DouBao model
    "DouBaoPro4KGenerateConfig",
    "DouBaoPro32KGenerateConfig",
    "DouBaoPro128KGenerateConfig",
    "DouBaoLite4KGenerateConfig",
    "DouBaoLite32KGenerateConfig",
    "DouBaoLite128KGenerateConfig",
]


class DouBaoPro4KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-pro-4k
    效果最好的主力模型，适合处理复杂任务，在参考问答、总结摘要、创作、文本分类、角色扮演等场景都有很好的效果。支持4k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-pro-4k", description="模型名称")


class DouBaoPro32KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-pro-32k
    效果最好的主力模型，适合处理复杂任务，在参考问答、总结摘要、创作、文本分类、角色扮演等场景都有很好的效果。支持32k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-pro-32k", description="模型名称")


class DouBaoPro128KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-pro-128k
    效果最好的主力模型，适合处理复杂任务，在参考问答、总结摘要、创作、文本分类、角色扮演等场景都有很好的效果。支持128k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-pro-128k", description="模型名称")


class DouBaoLite4KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-lite-4k
    Doubao-lite拥有极致的响应速度，更好的性价比，为客户不同场景提供更灵活的选择。支持4k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-lite-4k", description="模型名称")


class DouBaoLite32KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-lite-32k
    Doubao-lite拥有极致的响应速度，更好的性价比，为客户不同场景提供更灵活的选择。支持32k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-lite-32k", description="模型名称")


class DouBaoLite128KGenerateConfig(OpenAIGenerateConfig):
    """ Doubao-lite-128k
    Doubao-lite 拥有极致的响应速度，更好的性价比，为客户不同场景提供更灵活的选择。支持128k上下文窗口的推理和精调。
    """
    model: Optional[str] = Field(default="Doubao-lite-128k", description="模型名称")


TypeDouBaoGenerate = Union[
    OpenAIGenerateConfig,
    DouBaoPro4KGenerateConfig,
    DouBaoPro32KGenerateConfig,
    DouBaoPro128KGenerateConfig,
    DouBaoLite4KGenerateConfig,
    DouBaoLite32KGenerateConfig,
    DouBaoLite128KGenerateConfig,
]
