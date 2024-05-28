from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message


__all__ = [
    # Type
    "TypeAtomGenerate",
    # Atom model
    "AtomGenerateConfig",
    "Atom1BGenerateConfig",
    "Atom7BGenerateConfig",
    "Atom13BGenerateConfig",
    "Llama3Chinese8BInstruct",
]


class AtomGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(default=[])
    model: Optional[str] = Field(default=None, description="模型名称")
    top_p: Optional[float] = Field(default=0.95, description="""
            生成过程中核采样方法概率阈值。取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高。
            取值为0.8时，仅保留概率加起来大于等于0.8的最可能token的最小集合作为候选集。
            """)
    temperature: Optional[float] = Field(default=0.3, description="""
            用于控制随机性和多样性的程度。具体来说，temperature值控制了生成文本时对每个候选词的概率分布进行平滑的程度。
            较高的temperature值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；
            而较低的temperature值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。
            取值范围： [0, 2)，不建议取值为0，无意义。
            """)
    frequency_penalty: Optional[float] = Field(default=0, description="""
            默认为 0。介于 -2.0 和 2.0 之间的数字。正值会根据新标记在迄今为止的文本中出现的频率惩罚新标记，增加模型谈论新话题的可能性。
            """)
    stream: Optional[bool] = Field(default=False, description="""
            是否使用流式输出。当以stream模式输出结果时，接口返回结果为generator，需要通过迭代获取结果，默认每次输出为当前生成的整个序列，
            最后一次输出为最终全部生成结果，可以通过参数incremental_output为False改变输出模式为非增量输出。
            """)


class Atom1BGenerateConfig(AtomGenerateConfig):
    """ Atom-1B-Chat """
    model: Optional[str] = Field(default="Atom-1B-Chat", description="模型名称")


class Atom7BGenerateConfig(AtomGenerateConfig):
    """ Atom-7B-Chat """
    model: Optional[str] = Field(default="Atom-7B-Chat", description="模型名称")


class Atom13BGenerateConfig(AtomGenerateConfig):
    """ Atom-13B-Chat """
    model: Optional[str] = Field(default="Atom-13B-Chat", description="模型名称")


class Llama3Chinese8BInstruct(AtomGenerateConfig):
    """ Llama3-Chinese-8B-Instruct """
    model: Optional[str] = Field(default="Llama3-Chinese-8B-Instruct", description="模型名称")


TypeAtomGenerate = Union[
    AtomGenerateConfig,
    Atom1BGenerateConfig,
    Atom7BGenerateConfig,
    Atom13BGenerateConfig,
    Llama3Chinese8BInstruct,
]
