from typing import Any, List, Dict, Type, Union, Callable, Optional, Iterable
from pydantic import BaseModel, Field, ConfigDict
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from zlai.types.generate_config.completion import TypeGenerateConfig
from zlai.types.generate_config.image import TypeImageGenerateConfig
from zlai.types.generate_config.audio import TypeAudioGenerateConfig


__all__ = [
    "ModelConfig",
    "ToolsConfig",
    "InferenceMethod",
]


class ToolsConfig(BaseModel):
    """"""
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = Field(default='none', description="")
    tools: Optional[Union[Iterable[ChatCompletionToolParam], List[Dict]]] = Field(default=None, description="")


class InferenceMethod(BaseModel):
    """"""
    base: Optional[Callable] = None
    stream: Optional[Callable] = None


class ModelConfig(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: Optional[str] = Field(default=None, description="")
    model_path: Optional[str] = Field(default=None, description="")
    model_type: Optional[str] = Field(default=None, description="")
    load_method: Optional[Union[str, Callable]] = Field(default=None, description="")
    max_memory: Optional[Dict[Union[str, int], str]] = Field(default={0: "20GB"}, description="")
    generate_method: Optional[Union[
        Type[TypeGenerateConfig], Type[TypeAudioGenerateConfig], Type[TypeImageGenerateConfig]]] = Field(
        default=None, description="")
    inference_method: Optional[InferenceMethod] = Field(default=None, description="")

    def __init__(self, **data):
        super().__init__(**data)

    def get(self, key: Any):
        return self.model_dump().get(key)

    def update_kwargs(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.model_copy(update=kwargs)
