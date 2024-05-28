from pydantic import Field
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import Message

__all__ = [
    # Type
    "TypeYiGenerate",
    # Yi model
    "YiGenerateConfig",
    "YiLargeGenerateConfig",
    "YiMediumGenerateConfig",
    "YiVisionGenerateConfig",
    "YiMedium200KGenerateConfig",
    "YiSparkGenerateConfig",
    "YiLargeRAGGenerateConfig",
    "YiLargeTurboGenerateConfig",
    "YiLargePreviewGenerateConfig",
    "YiLargeRAGPreviewGenerateConfig",
]


class YiGenerateConfig(GenerateConfig):
    """"""
    messages: Union[List[Dict], List[Message]] = Field(default=[])
    model: Optional[str] = Field(default=None, description="模型名称")
    max_tokens: Optional[int] = Field(
        default=None, description="""
            指定模型在生成内容时token的最大数量，它定义了生成的上限，但不保证每次都会产生到这个数量。"""
    )
    stream: Optional[bool] = Field(default=False, description="""是否获取流式输出。""")
    temperature: Optional[float] = Field(
        default=0.3, description="""
            控制生成结果的发散性和集中性。数值越小，越集中；数值越大，越发散。取值范围：0到2之间。
            """
    )
    top_p: Optional[float] = Field(
        default=0.9, description="""
            控制生成结果的随机性。数值越小，随机性越弱；数值越大，随机性越强。取值范围：0到1之间。
            """
    )
    stop: Optional[List[str]] = Field(
        default=None, description="""
            停止词，当全匹配这个（组）词后会停止输出，这个（组）词本身不会输出。
            最多不能超过 5 个字符串，每个字符串不得超过 32 字节
            List[String]
            """
    )


class YiLargeGenerateConfig(YiGenerateConfig):
    """
    yi-large 16K
    全新千亿参数模型，提供超强问答及文本生成能力。
    适合于复杂语言理解和深度内容创作设计场景。
    ¥20 / 1M token
    """
    model: Optional[str] = Field(default="yi-large", description="模型名称")


class YiMediumGenerateConfig(YiGenerateConfig):
    """
    yi-medium	16K
    中型尺寸模型升级微调，能力均衡，性价比高。深度优化指令遵循能力。
    适用于日常聊天、问答、写作、翻译等通用场景，是企业级应用和AI大规模部署的理想选择。
    ¥2.5 / 1M token
    """
    model: Optional[str] = Field(default="yi-medium", description="模型名称")


class YiVisionGenerateConfig(YiGenerateConfig):
    """
    yi-vision	4K
    复杂视觉任务模型，提供高性能图片理解、分析能力。
    适合需要分析和解释图像、图表的场景，如图片问答、图表理解、OCR、视觉推理、教育、研究报告理解或多语种文档阅读等。
    ¥6 / 1M token
    """
    model: Optional[str] = Field(default="yi-vision", description="模型名称")


class YiMedium200KGenerateConfig(YiGenerateConfig):
    """
    yi-medium-200k	200K
    200K超长上下文窗口，提供长文本深度理解和生成能力。
    适用于长文本的理解和生成，如文档阅读、问答、构建知识库等场景。
    ¥12 / 1M token
    """
    model: Optional[str] = Field(default="yi-medium-200k", description="模型名称")


class YiSparkGenerateConfig(YiGenerateConfig):
    """
    yi-spark
    16K	小而精悍，轻量极速模型。提供强化数学运算和代码编写能力。
    适用于轻量化数学分析、代码生成、文本聊天等场景。
    ¥1 / 1M token
    """
    model: Optional[str] = Field(default="yi-spark", description="模型名称")


class YiLargeRAGGenerateConfig(YiGenerateConfig):
    """
    yi-large-rag	16K
    基于Yi-Large超强模型的高阶服务，结合检索与生成技术提供精准答案，支持客⼾私有知识库（请联系客服申请）。
    适用于需要实时信息扩展的复杂推理场景。
    ¥25 / 1M token
    """
    model: Optional[str] = Field(default="yi-large-rag", description="模型名称")


class YiLargeTurboGenerateConfig(YiGenerateConfig):
    """
    yi-large-turbo	16K
    超高性价比、卓越性能。根据性能和推理速度、成本，进行平衡性高精度调优。
    适用于全场景、高品质的推理及文本生成等场景。
    ¥12 / 1M token
    """
    model: Optional[str] = Field(default="yi-large-turbo", description="模型名称")


class YiLargePreviewGenerateConfig(YiGenerateConfig):
    """
    yi-large-preview	16K
    兼容版本模型文本推理能力增强。
    适用于复杂业务场景的文本处理。
    ¥20 / 1M token
    """
    model: Optional[str] = Field(default="yi-large-preview", description="模型名称")


class YiLargeRAGPreviewGenerateConfig(YiGenerateConfig):
    """
    yi-large-rag-preview	16K
    兼容版本模型实时信息获取，以及文本推理能力增强。
    适用于需要实时信息扩展的复杂业务场景的文本处理。
    ¥25 / 1M token
    """
    model: Optional[str] = Field(default="yi-large-rag-preview", description="模型名称")


TypeYiGenerate = Union[
    YiGenerateConfig,
    YiLargeGenerateConfig,
    YiMediumGenerateConfig,
    YiVisionGenerateConfig,
    YiMedium200KGenerateConfig,
    YiSparkGenerateConfig,
    YiLargeRAGGenerateConfig,
    YiLargeTurboGenerateConfig,
    YiLargePreviewGenerateConfig,
    YiLargeRAGPreviewGenerateConfig,
]
