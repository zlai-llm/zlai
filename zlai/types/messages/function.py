from pandas import DataFrame
from pydantic import Field, ConfigDict
from typing import Literal, Optional, Union, Dict, List
from zlai.types.messages.display.display import show_observation
from .base import Message


__all__ = [
    "ObservationMessage",
    "FunctionMessage",
    "ToolsMessage",
]


class ObservationMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["observation"] = Field(default="observation", description="角色")
    content: Union[str, List, Dict, DataFrame] = Field(..., description="对话内容")

    def show_streamlit(self) -> None:
        _ = self._validate_streamlit()
        show_observation(self.content)


class FunctionMessage(Message):
    """"""
    role: Literal["function"] = Field(default="function", description="角色")
    content: Union[str] = Field(default=None, description="对话内容")
    name: Optional[str] = Field(default="", description="""The name of the function to call.""")

    def show_streamlit(self) -> None:
        _ = self._validate_streamlit()
        show_observation(self.content)


class ToolsMessage(Message):
    """"""
    role: Literal["tool"] = Field(default="tool", description="角色")
    content: str = Field(default=None, description="对话内容")
    name: Optional[str] = Field(default="", description="""The name of the function to call.""")
    tool_call_id: Optional[Union[int, str, dict]] = Field(default="", description="id")

    def show_streamlit(self) -> None:
        _ = self._validate_streamlit()
        show_observation(self.content)
