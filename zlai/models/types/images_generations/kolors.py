from PIL.Image import Image as TypeImage
from typing import Optional
from pydantic import Field
from .base import ImageGenerateConfig


__all__ = [
    "KolorsImageGenerateConfig",
    "KolorsImage2ImageGenerateConfig",
]


class KolorsImageGenerateConfig(ImageGenerateConfig):
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


class KolorsImage2ImageGenerateConfig(ImageGenerateConfig):
    """"""
    image: TypeImage = Field(description="The image to use as the input for the image-to-image generation.")
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
            "image": self.image,
            "height": self.height,
            "width": self.width,
        }
