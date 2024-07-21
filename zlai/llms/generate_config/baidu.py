from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message


__all__ = [
    "TypeBaiduGenerate",
    "BaiduGenerateConfig",
    # ernie-4
    # "Ernie4Turbo8KGenerateConfig",
    # ernie-speed
    "ErnieSpeed8KGenerateConfig",
    "ErnieSpeed128KGenerateConfig",
    "ErnieSpeedAppBuilderGenerateConfig",
    # ernie-lite
    "ErnieLite8KGenerateConfig",
    "ErnieLite8K0922GenerateConfig",
    # ernie-tiny
    "ErnieTiny8KGenerateConfig",
]


class BaiduGenerateConfig(GenerateConfig):
    """"""
    messages: Union[str, List[str], List[int], object, None] = []
    temperature: Optional[float] = Field(
        default=0.8, description="较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定；默认0.8，范围 (0, 1.0]，不能为0")
    top_p: Optional[float] = Field(
        default=0.8, description="（1）影响输出文本的多样性，取值越大，生成文本的多样性越强（2）默认0.8，取值范围 [0, 1.0]")
    penalty_score: Optional[float] = Field(
        default=1.0, description="通过对已生成的token增加惩罚，减少重复生成的现象。说明：（1）值越大表示惩罚越大（2）默认1.0，取值范围：[1.0, 2.0]")
    stream: Optional[bool] = Field(
        default=False, description="是否以流式接口的形式返回数据，默认false")
    system: Optional[str] = Field(
        default=None, description="模型人设，主要用于人设设定，例如，你是xxx公司制作的AI助手，说明：（1）长度限制，message中的content总长度和system字段总内容不能超过20000个字符，且不能超过5120 tokens")
    user_id: Optional[str] = Field(
        default=None, description="表示最终用户的唯一标识符")


class ErnieSpeed8KGenerateConfig(BaiduGenerateConfig):
    """ERNIE-Speed-8K"""
    model: Optional[str] = Field(default="ERNIE-Speed-8K", description="模型名称")
    max_output_tokens: Optional[int] = Field(default=1024, description="指定模型最大输出token数，说明：（1）如果设置此参数，范围[2, 2048]（2）如果不设置此参数，最大输出token数为1024")


class ErnieSpeed128KGenerateConfig(BaiduGenerateConfig):
    """ERNIE-Speed-128K"""
    model: Optional[str] = Field(default="ERNIE-Speed-128K", description="模型名称")
    max_output_tokens: Optional[int] = Field(default=1024, description="指定模型最大输出token数，说明：（1）如果设置此参数，范围[2, 2048]（2）如果不设置此参数，最大输出token数为1024")


class ErnieSpeedAppBuilderGenerateConfig(BaiduGenerateConfig):
    """ERNIE Speed-AppBuilder"""
    model: Optional[str] = Field(default="ERNIE Speed-AppBuilder", description="模型名称")


class ErnieLite8KGenerateConfig(BaiduGenerateConfig):
    """ERNIE-Lite-8K"""
    model: Optional[str] = Field(default="ERNIE-Lite-8K", description="模型名称")
    max_output_tokens: Optional[int] = Field(default=1024, description="指定模型最大输出token数，说明：（1）如果设置此参数，范围[2, 2048]（2）如果不设置此参数，最大输出token数为1024")


class ErnieLite8K0922GenerateConfig(BaiduGenerateConfig):
    """ERNIE-Lite-8K-0922"""
    model: Optional[str] = Field(default="ERNIE-Lite-8K-0922", description="模型名称")


class ErnieTiny8KGenerateConfig(BaiduGenerateConfig):
    """ERNIE-Tiny-8K"""
    model: Optional[str] = Field(default="ERNIE-Tiny-8K", description="模型名称")
    min_output_tokens: Optional[int] = Field(
        default=None, description="指定模型最小输出token数，说明：该参数取值范围[2, 2048]")
    frequency_penalty: Optional[float] = Field(
        default=0.1, description="正值根据迄今为止文本中的现有频率对新token进行惩罚，从而降低模型逐字重复同一行的可能性；说明：默认0.1，取值范围[-2.0, 2.0]")
    presence_penalty: Optional[float] = Field(
        default=0.0, description="正值根据token记目前是否出现在文本中来对其进行惩罚，从而增加模型谈论新主题的可能性；说明：默认0.0，取值范围[-2.0, 2.0]")


class Ernie4Turbo8KGenerateConfig(BaiduGenerateConfig):
    """ERNIE-4.0-Turbo-8K"""
    model: Optional[str] = Field(default="ERNIE-4.0-Turbo-8K", description="模型名称")
    enable_system_memory: Optional[bool] = Field(
        default=False, description="是否开启系统记忆，说明：（1）false：未开启，默认false（2）true：表示开启，开启后，system_memory_id字段必填")
    system_memory_id: Optional[str] = Field(
        default=None, description="系统记忆ID，用于读取对应ID下的系统记忆，读取到的记忆文本内容会拼接message参与请求推理")
    disable_search: Optional[bool] = Field(
        default=False, description="是否强制关闭实时搜索功能，默认false，表示不关闭")
    enable_citation: Optional[bool] = Field(
        default=False, description="是否开启上角标返回，说明：（1）开启后，有概率触发搜索溯源信息search_info，search_info内容见响应参数介绍（2）默认false，不开启")
    enable_trace: Optional[bool] = Field(
        default=False, description="是否开启搜索溯源功能，说明：（1）开启后，有概率触发搜索溯源信息search_info，search_info内容见响应参数介绍（2）默认false，不开启")
    response_format: Optional[str] = Field(
        default=None, description="指定响应内容的格式，说明：（1）可选值：· json_object：以json格式返回，可能出现不满足效果情况· text：以文本格式返回")


TypeBaiduGenerate = Union[
    BaiduGenerateConfig,

    ErnieSpeed8KGenerateConfig,
    ErnieSpeed128KGenerateConfig,
    ErnieSpeedAppBuilderGenerateConfig,
    ErnieLite8KGenerateConfig,
    ErnieLite8K0922GenerateConfig,
    ErnieTiny8KGenerateConfig,
    # Ernie4Turbo8KGenerateConfig,
]
