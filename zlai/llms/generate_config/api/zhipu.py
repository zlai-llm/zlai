from pydantic import BaseModel, Field
from typing import Optional, Union, List
from zlai.llms.generate_config.base import GenerateConfig


__all__ = [
    "TypeZhipuGenerate",
    # zhipu
    "GLM4GenerateConfig",
    "GLM4PlusGenerateConfig",
    "GLM4LongGenerateConfig",
    "GLM40520GenerateConfig",
    "GLM4AirGenerateConfig",
    "GLM4AirXGenerateConfig",
    "GLM4FlashGenerateConfig",
    "GLM4FlashXGenerateConfig",
    "GLM3TurboGenerateConfig",
    "CodeGeexGenerateConfig",
    "GLM4AllToolsGenerateConfig",
    "GLM4VGenerateConfig",
    "GLM4VPlusGenerateConfig",
]


class ZhipuGenerateConfig(GenerateConfig):
    """"""
    messages: Union[str, List[str], List[int], object, None] = []
    do_sample: Optional[bool] = Field(
        default=True, description="do_sample 为 true 时启用采样策略，do_sample 为 false 时采样策略 temperature、top_p 将不生效")
    stream: Optional[bool] = Field(
        default=False, description="使用同步调用时，此参数应当设置为 fasle 或者省略。表示模型生成完所有内容后一次性返回所有内容。如果设置为 true，模型将通过标准 Event Stream ，逐块返回模型生成内容。")
    temperature: Optional[float] = Field(
        default=0.95, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0，默认值为 0.95，值越大，会使输出更随机，更具创造性；值越小，输出会更加稳定或确定建议您根据应用场景调整 top_p 或 temperature 参数，但不要同时调整两个参数")
    top_p: Optional[float] = Field(
        default=0.7, description="用温度取样的另一种方法，称为核取样取值范围是：(0.0, 1.0) 开区间，不能等于 0 或 1，默认值为 0.7模型考虑具有 top_p 概率质量 tokens 的结果")
    max_tokens: Optional[int] = Field(
        default=1024, description="模型输出最大 tokens，最大输出为8192，默认值为1024")
    stop: Optional[List[str]] = Field(
        default=None, description="否模型在遇到stop所制定的字符时将停止生成，目前仅支持单个停止词，格式为['stop_word1']")
    tools: Optional[List] = Field(
        default=None, description="可供模型调用的工具。默认开启web_search ，调用成功后作为参考信息提供给模型。注意：返回结果作为输入也会进行计量计费，每次调用大约会增加1000 tokens的消耗。"
    )
    tool_choice: Optional[str] = Field(
        default="auto", description="用于控制模型是如何选择要调用的函数，仅当工具类型为function时补充。默认为auto，当前仅支持auto"
    )


class GLM4GenerateConfig(ZhipuGenerateConfig):
    """
    100RMB / 1M tokens
    """
    model: str = "glm-4"


class GLM4PlusGenerateConfig(ZhipuGenerateConfig):
    """
    glm-4-plus
    """
    model: str = "glm-4-plus"


class GLM4LongGenerateConfig(ZhipuGenerateConfig):
    """
    100RMB / 1M tokens
    """
    model: str = "glm-4-long"


class GLM40520GenerateConfig(ZhipuGenerateConfig):
    """
    glm-4-0520
    """
    model: str = "glm-4-0520"


class GLM4AirGenerateConfig(ZhipuGenerateConfig):
    """
    1RMB / 1M tokens
    """
    model: str = "glm-4-air"


class GLM4AirXGenerateConfig(ZhipuGenerateConfig):
    """
    Air 极速版
    10RMB / 1M tokens
    """
    model: str = "glm-4-airx"


class GLM4FlashGenerateConfig(ZhipuGenerateConfig):
    """
    Flash 最实惠
    0.1RMB / 1M tokens
    """
    model: str = "glm-4-flash"


class GLM4FlashXGenerateConfig(ZhipuGenerateConfig):
    """
    Flash 最实惠
    0.1RMB / 1M tokens
    """
    model: str = "glm-4-flashx"


class GLM3TurboGenerateConfig(ZhipuGenerateConfig):
    """
    1RMB / 1M tokens
    """
    model: str = "glm-3-turbo"


class CodeGeexGenerateConfig(ZhipuGenerateConfig):
    """"""
    model: str = "codegeex-4"
    stop: Optional[List[str]] = Field(
        default=["<|endoftext|>", "<|user|>", "<|assistant|>", "<|observation|>"],
        description="否模型在遇到stop所制定的字符时将停止生成，目前仅支持单个停止词，格式为['stop_word1']")


class GLM4AllToolsGenerateConfig(ZhipuGenerateConfig):
    """"""
    model: str = "glm-4-alltools"


class GLM4VGenerateConfig(ZhipuGenerateConfig):
    """"""
    model: str = "glm-4v"
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.6


class GLM4VPlusGenerateConfig(ZhipuGenerateConfig):
    """"""
    model: str = "glm-4v-plus"
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.6


TypeZhipuGenerate = Union[
    ZhipuGenerateConfig,
    GLM4GenerateConfig,
    GLM4PlusGenerateConfig,
    GLM4LongGenerateConfig,
    GLM40520GenerateConfig,
    GLM4AirGenerateConfig,
    GLM4AirXGenerateConfig,
    GLM4FlashGenerateConfig,
    GLM4FlashXGenerateConfig,
    GLM3TurboGenerateConfig,
    CodeGeexGenerateConfig,
    GLM4AllToolsGenerateConfig,
    GLM4VGenerateConfig,
    GLM4VPlusGenerateConfig,
]
