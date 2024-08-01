import os
import re
import base64
import requests
from PIL import Image
from io import BytesIO
from PIL.Image import Image as TypeImage
from typing import List, Dict, Union, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
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


class ImageMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Optional[str] = Field(default="user", description="角色")
    image: Optional[Union[str, TypeImage]] = Field(default=None, description="图片")

    def parse_content(self):
        """"""
        from bs4 import BeautifulSoup
        if self.content:
            soup = BeautifulSoup(self.content, 'html.parser')
            img_tags = soup.find_all('img')
            if img_tags:
                self.image = img_tags[-1].get('src')
                self.content = soup.get_text()

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

    def load_url(self, url: str):
        """"""
        response = requests.get(url)
        if response.status_code == 200:
            image_base64 = base64.b64encode(response.content)
            self.image = image_base64.decode('utf-8')

    def read_image(self, path: str):
        """"""
        with open(path, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read())
        self.image = image_base64.decode('utf-8')

    def write_image(self, data: str, path: str):
        """"""
        binary_data = base64.b64decode(data)
        image = Image.open(BytesIO(binary_data))
        image.save(path)

    def add_image(
            self,
            path: Optional[str] = None,
            url: Optional[str] = None,
    ):
        """"""
        if path is not None:
            self.read_image(path=path)
        elif url is not None:
            self.load_url(url=url)
        else:
            raise ValueError("Either path or url must be provided.")
        self.content = f"{self.content}<image: {self.image}>"
        return self

    def split_image(self):
        """"""
        pattern = r"<image: (.*?)>"
        match = re.search(pattern, self.content)
        if match:
            image_bytes = base64.b64decode(match.group(1))
            self.image = Image.open(BytesIO(image_bytes)).convert('RGB')
            self.content = re.sub(pattern, "", self.content)
        return self


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
