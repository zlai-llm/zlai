import os
import base64
import requests
from PIL import Image
from io import BytesIO
from PIL.Image import Image as TypeImage
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Union, List, Dict
from zlai.utils.image import *
from zlai.utils import pkg_config
from .base import Message


__all__ = [
    "ImageUrl",
    "TextContent",
    "ImageContent",
    "ImageMixin",
    "ImageMessage",
]


class TextContent(BaseModel):
    """"""
    type: Literal["text"] = "text"
    text: Optional[str] = None


class ImageUrl(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    url: Optional[Union[str, TypeImage]] = None


class ImageContent(BaseModel):
    """"""
    type: Literal["image_url"] = "image_url"
    image_url: Optional[ImageUrl] = None


class ImageMixin(Message):
    """"""
    def load_path(self, ) -> bool:
        """"""
        if self.image is not None and os.path.exists(self.image):
            self.read_image(path=self.image)
            return True
        else:
            return False

    def _validate_image_path(self):
        """"""
        _image_path = os.path.join(pkg_config.cache_path, "image")
        if not os.path.exists(_image_path):
            os.makedirs(_image_path)

    def load_url(self, url: str) -> Union[str, None]:
        """"""
        response = requests.get(url)
        if response.status_code == 200:
            image_base64 = base64.b64encode(response.content)
            image = image_base64.decode('utf-8')
            return image
        else:
            raise Exception(f"Failed to load image from url: {url}")

    def read_image(self, path: str) -> Union[str, None]:
        """"""
        with open(path, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read())
        image = image_base64.decode('utf-8')
        return image

    def write_image(self, data: str, path: str):
        """"""
        binary_data = base64.b64decode(data)
        image = Image.open(BytesIO(binary_data))
        image.save(path)


class ImageMessage(ImageMixin):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user"] = Field(default="user", description="""The role of the author of this message.""")
    content: Optional[Union[str, List[Union[TextContent, ImageContent]]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(
            self,
            images: Optional[List[TypeImage]] = None,
            images_url: Optional[List[str]] = None,
            images_path: Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        _content = None
        if isinstance(self.content, str):
            _content = [self._add_content(self.content)]

            if images:
                for image in images:
                    _content.append(self._add_image(image))
            if images_url:
                for url in images_url:
                    _content.append(self._add_url(url))
            if images_path:
                for path in images_path:
                    _content.append(self._add_path(path))

        elif isinstance(self.content, list):
            _content = self.content

        self.content = _content

    def _add_content(self, content: str) -> TextContent:
        """"""
        return TextContent(text=content)

    def _add_image(self, image: TypeImage) -> ImageContent:
        """"""
        url = trans_image_to_bs64(image)
        return ImageContent(image_url=ImageUrl(url=url))

    def _add_url(self, url: str) -> ImageContent:
        """"""
        image = self.load_url(url=url)
        return ImageContent(image_url=ImageUrl(url=image))

    def _add_path(self, path: str) -> ImageContent:
        """"""
        image = self.read_image(path=path)
        return ImageContent(image_url=ImageUrl(url=image))

    def convert_image(self):
        """"""
        if isinstance(self.content, str):
            raise TypeError("content must be list")
        elif isinstance(self.content, list):
            for i, content in enumerate(self.content):
                if isinstance(content, ImageContent) and isinstance(content.image_url.url, str):
                    self.content[i].image_url.url = trans_bs64_to_image(content.image_url.url)

    def to_message(self, _type: Literal["mini_cpm", "glm4v"] = "mini_cpm") -> Dict:
        """"""
        if _type == "mini_cpm":
            _content = []
            if isinstance(self.content, str):
                _content.append(self.content)
            elif isinstance(self.content, list):
                question = ""
                for item in self.content:
                    if isinstance(item, TextContent):
                        question = item.text
                    if isinstance(item, ImageContent):
                        if isinstance(item.image_url.url, str):
                            _content.append(trans_bs64_to_image(item.image_url.url))
                        elif isinstance(item.image_url.url, TypeImage):
                            _content.append(item.image_url.url)
                        else:
                            raise TypeError(f"Url type error, but got {type(item.image_url.url)}")
                _content.append(question)

            return {"role": self.role, "content": _content}

        elif _type == "glm4v":
            question = ""
            image = None
            for item in self.content:
                if isinstance(item, TextContent):
                    question = item.text
                if isinstance(item, ImageContent):
                    if isinstance(item.image_url.url, str):
                        image = trans_bs64_to_image(item.image_url.url)
            message = dict(role=self.role, content=question)
            if image:
                message["image"] = image
            return message

        else:
            raise ValueError(f"Unknown message type {_type}")
