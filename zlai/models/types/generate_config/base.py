from typing import Optional
from pydantic import BaseModel, Field


__all__ = [
    "InferenceGenerateConfig"
]


class InferenceGenerateConfig(BaseModel):
    """"""
    max_length: Optional[int] = Field(default=None)
    max_new_tokens: Optional[int] = Field(default=None)
    top_k: Optional[int] = Field(default=None)
    top_p: Optional[float] = Field(default=None)
    do_sample: Optional[bool] = Field(default=True)
    temperature: Optional[float] = Field(default=None)

    def gen_kwargs(self):
        """"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
