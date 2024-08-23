from io import BytesIO
from pydantic import BaseModel, ConfigDict
from typing import Union, Literal, Optional
from PIL.Image import Image as TypeImage


__all__ = [
    "Content",
    "TypeImage",
    "TextContent",
    "ImageUrl",
    "ImageContent",
    "AudioContent",
    "ChartContent",
]


class Content(BaseModel):
    """"""
    type: str = "text"


class TextContent(Content):
    """"""
    type: Literal["text"] = "text"
    text: Optional[str] = None


class ImageUrl(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    url: Optional[Union[str, TypeImage]] = None


class ImageContent(Content):
    """"""
    type: Literal["image_url"] = "image_url"
    image_url: Optional[ImageUrl] = None


class AudioContent(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    type: Literal["audio"] = "audio"
    audio_url: Optional[Union[BytesIO, bytes, str]] = None


class ChartContent(Content):
    """"""
    type: Literal["chart"] = "chart"
    chart: Optional[str] = None
