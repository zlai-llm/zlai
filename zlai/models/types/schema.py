from typing import Type, List, Dict, Literal, Optional, Iterable
from pydantic import BaseModel, Field, ConfigDict
from openai.types.chat.completion_create_params import Function, FunctionCall
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from zlai.types.messages import TypeMessage
from .generate_config import *


__all__ = [
    "Message",
    "ModelConfig",
    "ChatCompletionRequest",
    "ToolsConfig",
]

ChatModel = Literal[
    "gpt-4-turbo",
]


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    messages: List[TypeMessage]
    model: Union[str, ChatModel]
    frequency_penalty: Optional[float] = Field(default=None, description="")
    function_call: FunctionCall = Field(default=None, description="")
    functions: Iterable[Function] = Field(default=None, description="")
    logit_bias: Optional[Dict[str, int]] = Field(default=None, description="")
    logprobs: Optional[bool] = Field(default=None, description="")
    max_tokens: Optional[int] = Field(default=None, description="")
    n: Optional[int] = Field(default=None, description="")
    presence_penalty: Optional[float] = Field(default=None, description="")
    seed: Optional[int] = Field(default=None, description="")
    stop: Union[Optional[str], List[str]] = Field(default=None, description="")
    stream: Optional[bool] = Field(default=False, description="")
    temperature: Optional[float] = Field(default=None, description="")
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = Field(default='none', description="")
    tools: Optional[Union[Iterable[ChatCompletionToolParam], List[Dict]]] = Field(default=None, description="")
    top_logprobs: Optional[int] = Field(default=None, description="")
    top_p: Optional[float] = Field(default=None, description="")


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
    load_method: Optional[str] = Field(default=None, description="")
    max_memory: Optional[Dict[Union[str, int], str]] = Field(default={0: "20GB"}, description="")
    generate_method: Optional[Union[str, Type[TypeInferenceGenerateConfig]]] = Field(default=None, description="")

    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.generate_method, str):
            generate_config_method = inference_generate_config_mapping.get(self.generate_method)
            if generate_config_method is not None:
                self.generate_method = generate_config_method

        if self.generate_method is None or isinstance(self.generate_method, str):
            self.generate_method = InferenceGenerateConfig
