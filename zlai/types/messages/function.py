from pandas import DataFrame
from pydantic import Field, ConfigDict
from typing import Literal, Optional, Union, Dict
from zlai.streamlit.utils.display import show_observation
from .base import Message


__all__ = [
    "ObservationMessage",
    "FunctionMessage",
    "ToolMessage",
    "ToolsMessage",
]


class ObservationMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["observation"] = Field("observation", description="角色")
    content: Union[str, Dict, DataFrame] = Field(..., description="对话内容")

    def show_streamlit(self) -> None:
        _ = self._validate_streamlit()
        show_observation(self.content)


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
