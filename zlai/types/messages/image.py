import os
import base64
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from pydantic import ConfigDict, Field
from typing import Optional, Literal, Tuple, Union, List, Dict
from zlai.utils.image import *
from zlai.utils import pkg_config
from .base import Message
from .content import TypeImage, ImageUrl, TextContent, ImageContent


__all__ = [
    "ImageMixin",
    "ImageMessage",
]


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
    role: Literal["user", "assistant"] = Field(default="user", description="""The role of the author of this message.""")
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
        _content = []
        if isinstance(self.content, list):
            _content = self.content
        elif isinstance(self.content, str):
            _content.append(self._add_content(self.content))
        if images:
            for image in images:
                _content.append(self._add_image(image))
        if images_url:
            for url in images_url:
                _content.append(self._add_url(url))
        if images_path:
            for path in images_path:
                _content.append(self._add_path(path))
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

    def to_dict(self) -> Dict:
        """"""
        return self.model_dump()

    def _mini_cpm_message(self) -> Dict:
        """"""
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

    def _glm4v_message(self) -> Dict:
        """"""
        message = dict(role=self.role)
        if isinstance(self.content, str):
            message["content"] = self.content
            return message
        elif isinstance(self.content, list):
            for item in self.content:
                if isinstance(item, TextContent):
                    message["content"] = item.text
                elif isinstance(item, ImageContent):
                    if isinstance(item.image_url.url, str):
                        message["image"] = trans_bs64_to_image(item.image_url.url)
                    elif isinstance(item.image_url.url, TypeImage):
                        message["image"] = item.image_url.url
            return message

    def _qwen2vl_message(self) -> Tuple[Dict, List[TypeImage]]:
        """"""
        images = []
        message = dict(role=self.role)
        if isinstance(self.content, str):
            message["content"] = self.content
            return message, images
        elif isinstance(self.content, list):
            content = []
            for item in self.content:
                if isinstance(item, TextContent):
                    content.append({"type": "text", "text": item.text})
                elif isinstance(item, ImageContent):
                    if isinstance(item.image_url.url, str):
                        image = trans_bs64_to_image(item.image_url.url)
                    elif isinstance(item.image_url.url, TypeImage):
                        image = item.image_url.url
                    else:
                        raise TypeError(f"Url type error, got type {type(item.image_url.url)}")
                    images.append(image)
                    content.append({"type": "image", "image": image})
            message["content"] = content
            return message, images

    def _ocr_message(self) -> Tuple[Dict, List[TypeImage]]:
        """"""
        images = []
        message = dict(role=self.role)
        if isinstance(self.content, str):
            message["content"] = self.content
            return message, images
        elif isinstance(self.content, list):
            content = []
            for item in self.content:
                if isinstance(item, TextContent):
                    content.append({"type": "text", "text": item.text})
                elif isinstance(item, ImageContent):
                    if isinstance(item.image_url.url, str):
                        image = trans_bs64_to_image(item.image_url.url)
                    elif isinstance(item.image_url.url, TypeImage):
                        image = item.image_url.url
                    else:
                        raise TypeError(f"Url type error, got type {type(item.image_url.url)}")
                    images.append(image)
                    content.append({"type": "image", "image": image})
            message["content"] = content
            return message, images

    def to_message(
            self,
            _type: Literal["mini_cpm", "glm4v", "qwen2vl", "ocr"] = "mini_cpm"
    ) -> Union[Dict, Tuple[Dict, List[TypeImage]]]:
        """"""
        if _type == "mini_cpm":
            return self._mini_cpm_message()
        elif _type == "glm4v":
            return self._glm4v_message()
        elif _type == "qwen2vl":
            return self._qwen2vl_message()
        elif _type == "ocr":
            return self._ocr_message()
        else:
            raise ValueError(f"Unknown message type {_type}")

    def is_path(self, path: str) -> bool:
        """"""
        return os.path.exists(path)

    def is_url(self, url: str) -> bool:
        """"""
        try:
            result = urlparse(url)
            mark = all([result.scheme, result.netloc])
        except Exception as e:
            mark = False
        return mark

    def show_streamlit(self):
        """"""
        st = self._validate_streamlit()
        if isinstance(self.content, str):
            st.markdown(self.content)
        if isinstance(self.content, list):
            for _content in self.content:
                if isinstance(_content, TextContent):
                    st.markdown(_content.text)
                elif isinstance(_content, ImageContent):
                    image = _content.image_url.url
                    if isinstance(image, str):
                        image = trans_bs64_to_image(image)
                    if isinstance(image, TypeImage):
                        st.image(image=image)
                    else:
                        st.write("Image can't be displayed.")
