from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message

__all__ = [
    # Type
    "TypeBaichuanGenerate",
    # Atom model
    "BaichuanGenerateConfig",
    "Baichuan2TurboGenerateConfig",
    "Baichuan2Turbo192kGenerateConfig",
]


class BaichuanGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(
        default=[], description="""
        对话消息列表 (历史对话按从老到新顺序填入)
        消息作者的角色，为以下其中之一 role-content
        1. user: 消息内容
        2. assistant: 消息内容
        """
    )
    model: Optional[str] = Field(
        default=None, description="""
        使用的模型 ID，模型列表：
        Baichuan2-Turbo
        Baichuan2-Turbo-192k
        """,
        examples=["Baichuan2-Turbo", "Baichuan2-Turbo-192k",],
    )
    stream: Optional[bool] = Field(
        default=False, description="""
        是否流式返回：默认 false, 可选 true
        """
    )
    temperature: Optional[float] = Field(
        default=0.3, description="""
        使用什么采样温度，介于 0 和 1 之间。较高的值（如 0.7）将使输出更加随机，
        而较低的值（如 0.2）将使其更加集中和确定性
        如果设置，值域须为 [0, 1] 我们推荐 0.3，以达到较合适的效果
        """
    )
    top_p: Optional[float] = Field(
        default=0.85, description="""
        取值范围: [.0f, 1.0f)。值越小，越容易出头部, 缺省 0.85
        """
    )
    top_k: Optional[int] = Field(
        default=5, description="""
        取值范围: [0, 20]。搜索采样控制参数，越大，采样集大, 0 则不走 top_k 采样筛选策略，最大 20(超过 20 会被修正成 20)，缺省 5
        """
    )
    max_tokens: Optional[int] = Field(
        default=2048, description="""
        回答产生的最大token数
        Baichuan2-Turbo，取值范围[1，8192]，默认取值2048
        Baichuan2-Turbo-192k，取值范围[1，2048]，默认取值2048
        """
    )
    with_search_enhance: Optional[bool] = Field(
        default=False, description="""
        开启web搜索增强，搜索增强会产生额外的费用, 缺省
        """)
    tools: Optional[List[Dict]] = Field(
        default=None, description="""
        可供模型调用的工具列表,目前支持retrieval
        """
    )


class Baichuan2TurboGenerateConfig(BaichuanGenerateConfig):
    """ Baichuan2-Turbo """
    model: Optional[str] = Field(
        default=None, description="""
            使用的模型 ID，模型列表：
            Baichuan2-Turbo
            Baichuan2-Turbo-192k
            """,
        examples=["Baichuan2-Turbo", "Baichuan2-Turbo-192k", ],
    )


class Baichuan2Turbo192kGenerateConfig(BaichuanGenerateConfig):
    """ Baichuan2-Turbo-192k """
    model: Optional[str] = Field(
        default=None, description="""
            使用的模型 ID，模型列表：
            Baichuan2-Turbo
            Baichuan2-Turbo-192k
            """,
        examples=["Baichuan2-Turbo", "Baichuan2-Turbo-192k", ],
    )


TypeBaichuanGenerate = Union[
    BaichuanGenerateConfig,
    Baichuan2TurboGenerateConfig,
    Baichuan2Turbo192kGenerateConfig,
]
