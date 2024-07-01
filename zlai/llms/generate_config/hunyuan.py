from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message


__all__ = [
    # Type
    "TypeHunYuanGenerate",
    # HunYuan model
    "HunYuanGenerateConfig",
    "HunYuanLiteGenerateConfig",
    "HunYuanStandardGenerateConfig",
    "HunYuanStandard256KGenerateConfig",
    "HunYuanProGenerateConfig",
]


class HunYuanGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(
        default=[],
        description="""聊天上下文信息。
            说明：
            1. 长度最多为 40，按对话时间从旧到新在数组中排列。
            2. Message.Role 可选值：system、user、assistant。
                其中，system 角色可选，如存在则必须位于列表的最开始。
                user 和 assistant 需交替出现（一问一答），以 user 提问开始和结束，且 Content 不能为空。
                Role 的顺序示例：[system（可选） user assistant user assistant user …]。
            3. Messages 中 Content 总长度不能超过模型输入长度上限（可参考 产品概述 文档），超过则会截断最前面的内容，只保留尾部内容。
        """
    )
    model: Optional[str] = Field(default=None, description="模型名称，可选值包括 hunyuan-lite、hunyuan-standard、hunyuan-standard-256K、hunyuan-pro。")
    stream: Optional[bool] = Field(
        default=False,
        description="""
            流式调用开关。
            说明：
                1. 未传值时默认为非流式调用（false）。
                2. 流式调用时以 SSE 协议增量返回结果（返回值取 Choices[n].Delta 中的值，需要拼接增量数据才能获得完整结果）。
                3. 非流式调用时：
            调用方式与普通 HTTP 请求无异。
            接口响应耗时较长，如需更低时延建议设置为 true。
            只返回一次最终结果（返回值取 Choices[n].Message 中的值）。
            
            注意：
                通过 SDK 调用时，流式和非流式调用需用不同的方式获取返回值，具体参考 SDK 中的注释或示例（在各语言 SDK 代码仓库的 examples/hunyuan/v20230901/ 目录中）。
            示例值：false
        """
    )
    stream_moderation: Optional[bool] = Field(
        default=False,
        description="""
            流式输出审核开关。
            说明：
            1. 当使用流式输出（Stream 字段值为 true）时，该字段生效。
            2. 输出审核有流式和同步两种模式，流式模式首包响应更快。未传值时默认为流式模式（true）。
            3. 如果值为 true，将对输出内容进行分段审核，审核通过的内容流式输出返回。如果出现审核不过，响应中的 FinishReason 值为 sensitive。
            4. 如果值为 false，则不使用流式输出审核，需要审核完所有输出内容后再返回结果。
            
            注意：
                当选择流式输出审核时，可能会出现部分内容已输出，但中间某一段响应中的 FinishReason 值为 sensitive，此时说明安全审核未通过。
                如果业务场景有实时文字上屏的需求，需要自行撤回已上屏的内容，并建议自定义替换为一条提示语，如 “这个问题我不方便回答，不如我们换个话题试试”，以保障终端体验。
            示例值：false
        """
    )
    top_p: Optional[float] = Field(
        default=None,
        description="""
            1. 影响输出文本的多样性，取值越大，生成文本的多样性越强。
            2. 取值区间为 [0.0, 1.0]，未传值时使用各模型推荐值。
            3. 非必要不建议使用，不合理的取值会影响效果。
        """
    )
    temperature: Optional[float] = Field(
        default=None,
        description="""
            1. 较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定。
            2. 取值区间为 [0.0, 2.0]，未传值时使用各模型推荐值。
            3. 非必要不建议使用，不合理的取值会影响效果。
        """
    )
    enable_enhancement: Optional[bool] = Field(
        default=None,
        description="""
            功能增强（如搜索）开关。
            说明：
                1. hunyuan-lite 无功能增强（如搜索）能力，该参数对 hunyuan-lite 版本不生效。
                2. 未传值时默认打开开关。
                3. 关闭时将直接由主模型生成回复内容，可以降低响应时延（对于流式输出时的首字时延尤为明显）。但在少数场景里，回复效果可能会下降。
                4. 安全审核能力不属于功能增强范围，不受此字段影响。
            示例值：true
        """
    )


class HunYuanLiteGenerateConfig(HunYuanGenerateConfig):
    """hunyuan-lite"""
    model: Optional[str] = Field(default="hunyuan-lite", description="模型名称")


class HunYuanStandardGenerateConfig(HunYuanGenerateConfig):
    """hunyuan-standard"""
    model: Optional[str] = Field(default="hunyuan-standard", description="模型名称")


class HunYuanStandard256KGenerateConfig(HunYuanGenerateConfig):
    """hunyuan-standard-256K"""
    model: Optional[str] = Field(default="hunyuan-standard-256K", description="模型名称")


class HunYuanProGenerateConfig(HunYuanGenerateConfig):
    """hunyuan-pro"""
    model: Optional[str] = Field(default="hunyuan-pro", description="模型名称")


TypeHunYuanGenerate = Union[
    HunYuanGenerateConfig,
    HunYuanLiteGenerateConfig,
    HunYuanStandardGenerateConfig,
    HunYuanStandard256KGenerateConfig,
    HunYuanProGenerateConfig,
]
