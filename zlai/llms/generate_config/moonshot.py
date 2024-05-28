from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message


__all__ = [
    # Type
    "TypeMoonShotGenerate",
    # Atom model
    "MoonShotGenerateConfig",
    "MoonShot8KV1GenerateConfig",
    "MoonShot32KV1GenerateConfig",
    "MoonShot128KV1GenerateConfig",
]


class MoonShotGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(
        default=[], description="""
        包含迄今为止对话的消息列表。
        这是一个结构体的列表，每个元素类似如下：{"role": "user", "content": "你好"} 
        role 只支持 system,user,assistant 其一，content 不得为空
        """
    )
    model: Optional[str] = Field(
        default=None, description="""
        模型名称，目前是 moonshot-v1-8k,moonshot-v1-32k,moonshot-v1-128k 其一
        """
    )
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
    temperature: Optional[float] = Field(
        default=0.3, description="""
        使用什么采样温度，介于 0 和 1 之间。较高的值（如 0.7）将使输出更加随机，
        而较低的值（如 0.2）将使其更加集中和确定性
        如果设置，值域须为 [0, 1] 我们推荐 0.3，以达到较合适的效果
        """
    )
    top_p: Optional[float] = Field(
        default=1.0, description="""
        另一种采样方法，即模型考虑概率质量为 top_p 的标记的结果。
        因此，0.1 意味着只考虑概率质量最高的 10% 的标记。
        一般情况下，我们建议改变这一点或温度，但不建议 同时改变
        """
    )
    n: Optional[int] = Field(
        default=1, description="""
        为每条输入消息生成多少个结果
        默认为 1，不得大于 5。特别的，当 temperature 非常小靠近 0 的时候，我们只能返回 1 个结果，
        如果这个时候 n 已经设置并且 > 1，我们的服务会返回不合法的输入参数(invalid_request_error)
        """,
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
    stream: Optional[bool] = Field(
        default=False, description="""
        是否流式返回：默认 false, 可选 true
        """
    )


class MoonShot8KV1GenerateConfig(MoonShotGenerateConfig):
    """ moonshot-v1-8k """
    model: Optional[str] = Field(
        default="moonshot-v1-8k",
        description="Model ID, 可以通过 List Models 获取",
        examples=['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k',],
    )


class MoonShot32KV1GenerateConfig(MoonShotGenerateConfig):
    """ moonshot-v1-32k """
    model: Optional[str] = Field(
        default="moonshot-v1-32k",
        description="Model ID, 可以通过 List Models 获取",
        examples=['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k',],
    )


class MoonShot128KV1GenerateConfig(MoonShotGenerateConfig):
    """ moonshot-v1-128k """
    model: Optional[str] = Field(
        default="moonshot-v1-128k",
        description="Model ID, 可以通过 List Models 获取",
        examples=['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k',],
    )


TypeMoonShotGenerate = Union[
    MoonShotGenerateConfig,
    MoonShot8KV1GenerateConfig,
    MoonShot32KV1GenerateConfig,
    MoonShot128KV1GenerateConfig,
]
