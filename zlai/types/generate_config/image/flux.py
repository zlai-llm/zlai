from typing import Optional, Union
from pydantic import Field
from .base import ImageGenerateConfig


__all__ = [
    "TypeFLUXGenerate",
    "FLUXImageGenerateConfig",
]


class FLUXImageGenerateConfig(ImageGenerateConfig):
    """"""
    height: Optional[int] = Field(default=1024, description="The height of the image to generate.")
    width: Optional[int] = Field(default=1024, description="The width of the image to generate.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "size" in kwargs:
            self.width, self.height = [int(item) for item in kwargs["size"].split("x")]

    def gen_kwargs(self) -> dict:
        """"""
        return {
            "prompt": self.prompt,
            "height": self.height,
            "width": self.width,
        }


TypeFLUXGenerate = Union[
    FLUXImageGenerateConfig
]
