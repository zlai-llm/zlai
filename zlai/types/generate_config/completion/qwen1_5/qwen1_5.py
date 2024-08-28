from pydantic import Field
from typing import Union, Optional
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeQwen15Generate",
    "Qwen15GenerateConfig",
    "Qwen15Chat7BGenerateConfig",
    "Qwen15Chat14BGenerateConfig",
    "Qwen15Chat72BAWQGenerateConfig",
    "Qwen15Chat72BGPTQInt4GenerateConfig",
    "Qwen15Chat72BGPTQInt8GenerateConfig",
]


class Qwen15GenerateConfig(GenerateConfig):
    """"""
    repetition_penalty: float = Field(default=1.05, description="")
    max_new_tokens: int = Field(default=2048, description="")
    do_sample: bool = Field(default=True, description="")
    temperature: float = Field(default=0.7, description="")
    top_p: float = Field(default=0.8, description="")
    top_k: int = Field(default=20, description="")
    stream: bool = Field(default=False, description="")
    incremental: Optional[bool] = Field(default=False, description="默认为 False，如果设置为 True，模型仅输出增量 token")


class Qwen15Chat7BGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen1.5-7B-Chat", description="模型名称")


class Qwen15Chat14BGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen1.5-14B-Chat", description="模型名称")


class Qwen15Chat72BAWQGenerateConfig(Qwen15GenerateConfig):
    """"""
    model: Optional[str] = Field(default="Qwen1.5-72B-Chat-AWQ", description="模型名称")


class Qwen15Chat72BGPTQInt4GenerateConfig(Qwen15GenerateConfig):
    model: Optional[str] = Field(default="Qwen1.5-72B-Chat-GPTQ-Int4", description="模型名称")


class Qwen15Chat72BGPTQInt8GenerateConfig(Qwen15GenerateConfig):
    model: Optional[str] = Field(default="Qwen1.5-72B-Chat-GPTQ-Int8", description="模型名称")


TypeQwen15Generate = Union[
    Qwen15GenerateConfig,
    Qwen15Chat7BGenerateConfig,
    Qwen15Chat14BGenerateConfig,
    Qwen15Chat72BAWQGenerateConfig,
    Qwen15Chat72BGPTQInt4GenerateConfig,
    Qwen15Chat72BGPTQInt8GenerateConfig,
]
