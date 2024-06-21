from dataclasses import dataclass
from typing import Union, Dict, List, Any
from pydantic import BaseModel, Field, field_validator


__all__ = [
    "Role",
    "SystemPrompt",
    "UserPrompt",
    "AssistantPrompt",
    "ToolsPrompt",
    "ChatPrompt",
    "ObservationPrompt",
    "ImagePrompt",
    "FewShot",
    "Message",
    "Messages",
    "SystemMessage",
    "UserMessage",
    "AssistantMessage",
    "ObservationMessage",
    "ToolsMessage",
]

prompt_system_tools_content = 'Answer the following questions as best as you can. You have access to the following tools:'


@dataclass
class Role:
    """"""
    system: str = "system"
    user: str = "user"
    assistant: str = "assistant"


class Message(BaseModel):
    """"""
    role: str = Field(default="", description="角色")
    content: str = Field(default="", description="对话内容")


class SystemPrompt(Message):
    """"""
    role: str = Field("system", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["system"]:
            raise ValueError(f"role must in ['system'], your role: `{role}`.")
        return role


class ToolsPrompt(Message):
    """"""
    role: str = Field("system", description="角色")
    content: str = Field(prompt_system_tools_content, description="对话内容")
    tools: Union[Dict] = {}

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["system"]:
            raise ValueError(f"role must in ['system'], your role: `{role}`.")
        return role


class ChatPrompt(Message):
    """
    desc: 对话格式
    """
    role: str = Field(..., description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["user", "assistant", "observation"]:
            raise ValueError(f"role must in ['user', 'assistant', 'observation'], your role: `{role}`.")
        return role


class ObservationPrompt(Message):
    """
    desc: 对话格式
    """
    role: str = Field("observation", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["observation"]:
            raise ValueError(f"role must in ['observation'], your role: `{role}`.")
        return role


class UserPrompt(Message):
    """"""
    role: str = Field("user", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["user"]:
            raise ValueError(f"role must in ['user'], your role: `{role}`.")
        return role


class AssistantPrompt(Message):
    """"""
    role: str = Field("assistant", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["assistant",]:
            raise ValueError(f"role must in ['assistant'], your role: `{role}`.")
        return role


class ImagePrompt(Message):
    """"""
    role: str = Field("user", description="角色")
    content: str = Field(..., description="对话内容")
    image: str = Field(..., description="图像地址")
    image_start_tag: str = "<img>"
    image_end_tag: str = "</img>"

    def from_list_format(self, list_format: List[Dict]):
        text = ''
        num_images = 0
        for ele in list_format:
            if 'image' in ele:
                num_images += 1
                text += f'Picture {num_images}: '
                text += self.image_start_tag + ele['image'] + self.image_end_tag
                text += '\n'
            elif 'text' in ele:
                text += ele['text']
            elif 'box' in ele:
                if 'ref' in ele:
                    text += self.ref_start_tag + ele['ref'] + self.ref_end_tag
                for box in ele['box']:
                    text += self.box_start_tag + '(%d,%d),(%d,%d)' % (box[0], box[1], box[2], box[3]) + self.box_end_tag
            else:
                raise ValueError("Unsupport element: " + str(ele))
        return text

    def _dict(self) -> Dict[str, Any]:
        """"""
        text = ''.join(['Picture 1: ', self.image_start_tag, self.image, self.image_end_tag, '\n', self.content])
        return UserPrompt(content=text).model_dump()

    def dict(  # noqa: D102
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return self._dict()

    def model_dump(
        self,
        *,
        mode: str = 'python',
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> Dict[str, Any]:
        return self._dict()


class Tools(BaseModel):
    """
    desc: 工具类

    >>> parameters = {
    >>>     "type": "object",
    >>>     "properties": {
    >>>         "symbol": {
    >>>             "description": "需要追踪的股票代码"
    >>>         }
    >>>     },
    >>>     "required": ['symbol']
    >>> }
    """
    name: str = "tools"
    description: str = "工具类"
    parameters: Dict = {
        "type": "object",
        "properties": {},
        "required": ['symbol'],
    }


class Messages(BaseModel):
    """"""
    messages: List[Message] = Field(default=[Message()], description="对话内容")


class SystemMessage(Message):
    """"""
    role: str = Field("system", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["system"]:
            raise ValueError(f"role must in ['system'], your role: `{role}`.")
        return role


class ToolsMessage(Message):
    """"""
    role: str = Field(default="tool", description="角色")
    content: str = Field(default="", description="对话内容")
    tool_call_id: Union[int, str, dict] = Field(default=None, description="id")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["tool"]:
            raise ValueError(f"role must in ['tool'], your role: `{role}`.")
        return role


class ChatMessage(Message):
    """
    desc: 对话格式
    """
    role: str = Field(..., description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["user", "assistant", "observation"]:
            raise ValueError(f"role must in ['user', 'assistant', 'observation'], your role: `{role}`.")
        return role


class ObservationMessage(Message):
    """
    desc: 对话格式
    """
    role: str = Field("observation", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["observation"]:
            raise ValueError(f"role must in ['observation'], your role: `{role}`.")
        return role


class UserMessage(Message):
    """"""
    role: str = Field("user", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["user"]:
            raise ValueError(f"role must in ['user'], your role: `{role}`.")
        return role


class AssistantMessage(Message):
    """"""
    role: str = Field("assistant", description="角色")
    content: str = Field(..., description="对话内容")

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["assistant",]:
            raise ValueError(f"role must in ['assistant'], your role: `{role}`.")
        return role


class FewShot(BaseModel):
    """"""
    few_shot: List[ChatPrompt]

