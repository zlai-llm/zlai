from typing import Optional
from pydantic import BaseModel, Field


__all__ = [
    "ImageGenerateConfig",
]


class ImageGenerateConfig(BaseModel):
    """"""
    prompt: Optional[str] = Field(default=None)

    def gen_kwargs(self):
        """"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
