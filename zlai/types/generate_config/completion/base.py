from typing import Optional
from pydantic import BaseModel, Field


__all__ = [
    "GenerateConfig",
]


class GenerateConfig(BaseModel):
    """"""
    max_length: Optional[int] = Field(default=None)
    max_new_tokens: Optional[int] = Field(default=None)
    top_k: Optional[int] = Field(default=None)
    do_sample: Optional[bool] = Field(
        default=None, description="do_sample 为 true 时启用采样策略，do_sample 为 false 时采样策略 temperature、top_p 将不生效")
    temperature: Optional[float] = Field(
        default=None, description="采样温度，控制输出的随机性，必须为正数取值范围是：(0.0, 1.0)，不能等于 0，值越大，会使输出更随机，更具创造性。")
    top_p: Optional[float] = Field(
        default=None, description="用温度取样的另一种方法，称为核取样取值范围是：(0.0, 1.0) 开区间，不能等于 0 或 1")

    def gen_kwargs(self):
        """"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
