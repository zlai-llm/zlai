from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict
from ...schema import Message


__all__ = [
    "GenerateConfig",
    "BaseGenerateConfig",
]


class GenerateConfig(BaseModel):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    messages: Union[List[Dict], List[Message]] = Field(default=[])


class BaseGenerateConfig(GenerateConfig):
    """"""
    max_length: Optional[int] = 1024
    max_new_tokens: Optional[int] = 512
    top_k: Optional[int] = 20
    top_p: Optional[float] = 0.8
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8
    stream: Optional[bool] = False
    incremental: Optional[bool] = Field(default=False, description="默认为 False，如果设置为 True，模型仅输出增量 token")
