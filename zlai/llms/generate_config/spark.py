from pydantic import Field
from typing import Optional, Union
from .openai import *


__all__ = [
    "TypeSparkGenerate",
    "SparkGenerateConfig",
    "SparkLiteGenerateConfig",
    "SparkV2GenerateConfig",
    "SparkProGenerateConfig",
    "SparkMaxGenerateConfig",
    "Spark4UltraGenerateConfig",
]


class SparkGenerateConfig(OpenAIGenerateConfig):
    """ Spark通用配置 """
    temperature: Optional[float] = Field(default=0.5, description="取值范围 (0，1] ，默认值0.5	核采样阈值。用于决定结果随机性，取值越高随机性越强即相同的问题得到的不同答案的可能性越高")
    max_tokens: Optional[int] = Field(default=4096, description="取值为[1,8192]，默认为4096。	模型回答的tokens的最大长度")
    # top_k: Optional[int] = Field(default=4, description="取值为[1，6],默认为4	从k个候选中随机选择⼀个（⾮等概率）")


class SparkLiteGenerateConfig(SparkGenerateConfig):
    """ general指向Lite版本； """
    model: Optional[str] = Field(default="general", description="模型名称")


class SparkV2GenerateConfig(SparkGenerateConfig):
    """ generalv2指向V2.0版本； """
    model: Optional[str] = Field(default="generalv2", description="模型名称")


class SparkProGenerateConfig(SparkGenerateConfig):
    """ generalv3指向Pro版本； """
    model: Optional[str] = Field(default="generalv3", description="模型名称")


class SparkMaxGenerateConfig(SparkGenerateConfig):
    """ generalv3.5指向Max版本； """
    model: Optional[str] = Field(default="generalv3.5", description="模型名称")


class Spark4UltraGenerateConfig(SparkGenerateConfig):
    """ 4.0Ultra指向4.0 Ultra版本； """
    model: Optional[str] = Field(default="4.0Ultra", description="模型名称")


TypeSparkGenerate = Union[
    SparkGenerateConfig,
    SparkLiteGenerateConfig,
    SparkV2GenerateConfig,
    SparkProGenerateConfig,
    SparkMaxGenerateConfig,
    Spark4UltraGenerateConfig,
]
