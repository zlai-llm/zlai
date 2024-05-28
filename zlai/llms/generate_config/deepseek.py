from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message


__all__ = [
    # Type
    "TypeDeepSeekGenerate",
    # DeepSeek model
    "DeepSeekGenerateConfig",
    "DeepSeekChatGenerateConfig",
    "DeepSeekCoderGenerateConfig",
]


class DeepSeekGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(default=[])
    model: Optional[str] = Field(default=None, description="模型名称")
    max_tokens: Optional[int] = Field(
        default=None, description="""
            聊天完成时生成的最大 token 数。如果到生成了最大 token 数个结果仍然没有结束，finish reason 会是 "length", 否则会是 "stop"

            这个值建议按需给个合理的值，如果不给的话，我们会给一个不错的整数比如 1024。
            特别要注意的是，这个 max_tokens 是指您期待我们返回的 token 长度，而不是输入 + 输出的总长度。
            比如对一个 moonshot-v1-8k 模型，它的最大输入 + 输出总长度是 8192，
            当输入 messages 总长度为 4096 的时候，您最多只能设置为 4096，
            否则我们服务会返回不合法的输入参数（ invalid_request_error ），并拒绝回答。
            如果您希望获得“输入的精确 token 数”，可以使用下面的“计算 Token” API 使用我们的计算器获得计数
            """
    )
    stream: Optional[bool] = Field(
        default=False, description="""
                是否使用流式输出。当以stream模式输出结果时，接口返回结果为generator，需要通过迭代获取结果，默认每次输出为当前生成的整个序列，
                最后一次输出为最终全部生成结果，可以通过参数incremental_output为False改变输出模式为非增量输出。
                """
    )
    temperature: Optional[float] = Field(
        default=0.3, description="""
                用于控制随机性和多样性的程度。具体来说，temperature值控制了生成文本时对每个候选词的概率分布进行平滑的程度。
                较高的temperature值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；
                而较低的temperature值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。
                取值范围： [0, 2)，不建议取值为0，无意义。
                """
    )
    top_p: Optional[float] = Field(
        default=0.95, description="""
            生成过程中核采样方法概率阈值。取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高。
            取值为0.8时，仅保留概率加起来大于等于0.8的最可能token的最小集合作为候选集。
            """
    )
    presence_penalty: Optional[float] = Field(
        default=0, description="""
            存在惩罚，介于-2.0到2.0之间的数字。正值会根据新生成的词汇是否出现在文本中来进行惩罚，
            增加模型讨论新话题的可能性，默认为 0
            """
    )
    frequency_penalty: Optional[float] = Field(
        default=0, description="""
            频率惩罚，介于-2.0到2.0之间的数字。正值会根据新生成的词汇在文本中现有的频率来进行惩罚，
            减少模型一字不差重复同样话语的可能性，默认为 0
            """
    )
    stop: Optional[List[str]] = Field(
        default=None, description="""
            停止词，当全匹配这个（组）词后会停止输出，这个（组）词本身不会输出。
            最多不能超过 5 个字符串，每个字符串不得超过 32 字节
            List[String]
            """
    )


class DeepSeekChatGenerateConfig(DeepSeekGenerateConfig):
    """ DeepSeek-Chat """
    model: Optional[str] = Field(default="deepseek-chat", description="模型名称")


class DeepSeekCoderGenerateConfig(DeepSeekGenerateConfig):
    """ DeepSeek-Coder """
    model: Optional[str] = Field(default="deepseek-coder", description="模型名称")


TypeDeepSeekGenerate = Union[
    DeepSeekGenerateConfig,
    DeepSeekChatGenerateConfig,
    DeepSeekCoderGenerateConfig,
]
