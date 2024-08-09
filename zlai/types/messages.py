import os
import base64
import requests
from PIL import Image
from io import BytesIO
from PIL.Image import Image as TypeImage
from typing import List, Dict, Union, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from zlai.utils.image import *
from zlai.utils import pkg_config
from .function_call import *


__all__ = [
    "Message",
    "ChatMessage",
    "SystemMessage",
    "SystemToolsMessage",
    "UserMessage",
    "AssistantMessage",
    "AssistantWithMetadataMessage",
    "ObservationMessage",
    "FunctionMessage",
    "ToolMessage",
    "ToolsMessage",
    "TextContent",
    "ImageUrl",
    "ImageContent",
    "ImageMessage",
    "ChatCompletionMessage",
    "TypeMessage",
]


class Message(BaseModel):
    """"""
    role: str = Field(default="", description="角色")
    content: str = Field(default="", description="对话内容")


class ChatMessage(Message):
    """"""
    role: str = Field(..., description="角色")
    content: str = Field(..., description="对话内容")


class SystemMessage(Message):
    """"""
    role: Literal["system"] = Field(default="system", description="角色")
    content: str = Field(..., description="对话内容")


class SystemToolsMessage(SystemMessage):
    """for glm4 function call"""
    tools: Optional[List[Dict]] = Field(default=None, description="工具列表")


class UserMessage(Message):
    """"""
    role: Literal["user"] = Field("user", description="角色")
    content: str = Field(..., description="对话内容")


class AssistantMessage(Message):
    """"""
    role: Literal["assistant"] = Field("assistant", description="角色")
    content: str = Field(..., description="对话内容")


class AssistantWithMetadataMessage(AssistantMessage):
    """for glm4 function call"""
    metadata: str = Field(default=None, description="metadata")
    content: str = Field(default="", description="对话内容")


class ObservationMessage(Message):
    """"""
    role: Literal["observation"] = Field("observation", description="角色")
    content: str = Field(..., description="对话内容")


class FunctionMessage(ObservationMessage):
    pass


class ToolMessage(ObservationMessage):
    """"""
    function_call: bool = Field(default=True, description="是否为工具调用")


class ToolsMessage(Message):
    """"""
    role: Literal["tool"] = Field(default="tool", description="角色")
    content: str = Field(default="", description="对话内容")
    tool_call_id: Optional[Union[int, str, dict]] = Field(default=None, description="id")


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


class TextContent(BaseModel):
    """"""
    type: str = "text"
    text: Optional[str] = None


class ImageUrl(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    url: Optional[Union[str, TypeImage]] = None


class ImageContent(BaseModel):
    """"""
    type: str = "image_url"
    image_url: Optional[ImageUrl] = None


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


class ChatCompletionMessage(BaseModel):
    """"""
    role: Literal["user", "assistant", "system", "tool"] = Field(..., description="""The role of the author of this message.""")
    content: Optional[str] = Field(default=None, description="""The contents of the message.""")
    function_call: Optional[FunctionCall] = Field(default=None, description="""
        Deprecated and replaced by `tool_calls`.
        The name and arguments of a function that should be called, as generated by the
        model.
    """)
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = Field(default=None, description="""
        The tool calls generated by the model, such as function calls.
    """)


TypeMessage = Union[
    Message,
    ChatMessage,
    SystemMessage,
    SystemToolsMessage,
    UserMessage,
    AssistantMessage,
    AssistantWithMetadataMessage,
    ObservationMessage,
    FunctionMessage,
    ToolMessage,
    ToolsMessage,
    ImageMessage,
    ChatCompletionMessage,
]
