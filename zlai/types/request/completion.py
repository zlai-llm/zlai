from typing import List, Dict, Union, Literal, Optional, Iterable
from pydantic import Field
from openai.types.chat.completion_create_params import Function, FunctionCall
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from zlai.types.messages import TypeMessage
from .base import BaseRequest


__all__ = [
    "ChatCompletionRequest",
]


ChatModel = Literal[
    "gpt-4-turbo",
]


class ChatCompletionRequest(BaseRequest):
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
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = Field(default='auto', description="")
    tools: Optional[Union[Iterable[ChatCompletionToolParam], List[Dict]]] = Field(default=None, description="")
    top_logprobs: Optional[int] = Field(default=None, description="")
    top_p: Optional[float] = Field(default=None, description="")
