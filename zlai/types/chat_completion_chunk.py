from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from .completion_usage import CompletionUsage
from .chat_completion_token_logprob import ChatCompletionTokenLogprob


__all__ = [
    "ChatCompletionChunk",
    "Choice",
    "ChoiceDelta",
    "ChoiceDeltaFunctionCall",
    "ChoiceDeltaToolCall",
    "ChoiceDeltaToolCallFunction",
    "ChoiceLogprobs",
]


class ChoiceDeltaFunctionCall(BaseModel):
    arguments: Optional[str] = None
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Optional[str] = None
    """The name of the function to call."""


class ChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Optional[str] = None
    """The name of the function to call."""


class ChoiceDeltaToolCall(BaseModel):
    index: int

    id: Optional[str] = None
    """The ID of the tool call."""

    function: Optional[ChoiceDeltaToolCallFunction] = None

    type: Optional[Literal["function"]] = None
    """The type of the tool. Currently, only `function` is supported."""


class ChoiceDelta(BaseModel):
    content: Optional[str] = None
    """The contents of the chunk message."""

    function_call: Optional[ChoiceDeltaFunctionCall] = None
    """Deprecated and replaced by `tool_calls`.

    The name and arguments of a function that should be called, as generated by the
    model.
    """

    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    """The role of the author of this message."""

    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChatCompletionTokenLogprob]] = None
    """A list of message content tokens with log probability information."""


class Choice(BaseModel):
    delta: ChoiceDelta
    """A chat completion delta generated by streamed model responses."""

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
    """The reason the model stopped generating tokens.

    This will be `stop` if the model hit a natural stop point or a provided stop
    sequence, `length` if the maximum number of tokens specified in the request was
    reached, `content_filter` if content was omitted due to a flag from our content
    filters, `tool_calls` if the model called a tool, or `function_call`
    (deprecated) if the model called a function.
    """

    index: int
    """The index of the choice in the list of choices."""

    logprobs: Optional[ChoiceLogprobs] = None
    """Log probability information for the choice."""


class ChatCompletionChunk(BaseModel):
    id: str
    """A unique identifier for the chat completion. Each chunk has the same ID."""

    choices: List[Choice]
    """A list of chat completion choices.

    Can contain more than one elements if `n` is greater than 1. Can also be empty
    for the last chunk if you set `stream_options: {"include_usage": true}`.
    """

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created.

    Each chunk has the same timestamp.
    """

    model: str
    """The model to generate the completion."""

    object: Literal["chat.completion.chunk"]
    """The object type, which is always `chat.completion.chunk`."""

    system_fingerprint: Optional[str] = None
    """
    This fingerprint represents the backend configuration that the model runs with.
    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """

    usage: Optional[CompletionUsage] = None
    """
    An optional field that will only be present when you set
    `stream_options: {"include_usage": true}` in your request. When present, it
    contains a null value except for the last chunk which contains the token usage
    statistics for the entire request.
    """
