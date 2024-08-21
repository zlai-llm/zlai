from typing import Any, List, Dict, Union, Callable, Optional, Iterable
from pydantic import BaseModel, Field, ConfigDict
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from zlai.types.generate_config.completion.base import GenerateConfig
from zlai.types.generate_config.image.base import ImageGenerateConfig
from zlai.types.generate_config.audio.base import VoiceGenerateConfig


__all__ = [
    "ModelConfig",
    "ToolsConfig",
]


class ToolsConfig(BaseModel):
    """"""
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = Field(default='none', description="")
    tools: Optional[Union[Iterable[ChatCompletionToolParam], List[Dict]]] = Field(default=None, description="")


class ModelConfig(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: Optional[str] = Field(default=None, description="")
    model_path: Optional[str] = Field(default=None, description="")
    model_type: Optional[str] = Field(default=None, description="")
    load_method: Optional[Union[str, Callable]] = Field(default=None, description="")
    max_memory: Optional[Dict[Union[str, int], str]] = Field(default={0: "20GB"}, description="")
    generate_method: Optional[Union[GenerateConfig, ImageGenerateConfig, VoiceGenerateConfig]] = Field(
        default=None, description="")

    def __init__(self, **data):
        super().__init__(**data)

    def get(self, key: Any):
        return self.model_dump().get(key)

    def update_kwargs(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.model_copy(update=kwargs)
