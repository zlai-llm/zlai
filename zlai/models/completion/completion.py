import time
from logging import Logger
from typing import Any, List, Dict, Iterable, Optional, Callable

from zlai.types import *
from zlai.types.chat.chat_completion import Choice as ChatChoice
from zlai.types.chat.chat_completion_chunk import Choice as ChunkChoice
from zlai.utils.mixin import LoggerMixin
from zlai.types.models_config import ModelConfig, ToolsConfig
from zlai.types.generate_config.completion import GenerateConfig
from zlai.models.utils import generate_id, stream_message_chunk
from .glm4 import *


__all__ = [
    "LoadModelCompletion",
]


class LoadModelCompletion(LoggerMixin):
    """"""
    model: Any
    tokenizer: Any
    model_config: Union[Dict, ModelConfig]
    load_method: Union[str, Callable]

    def __init__(
            self,
            model_path: Optional[str] = None,
            model_config: Optional[ModelConfig] = None,
            model_name: Optional[str] = None,
            generate_config: Optional[GenerateConfig] = None,
            tools_config: Optional[ToolsConfig] = None,
            load_method: Optional[str] = "auto",
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        self.model_path = model_path
        self.model_config = model_config
        self.model_name = model_name
        self.generate_config = generate_config
        self.tools_config = tools_config
        self.logger = logger
        self.verbose = verbose
        self.load_method = load_method
        self.args = args
        self.kwargs = kwargs
        self._logger(msg=f"[{__class__.__name__}] Model Name: {model_name}", color="blue")
        self._logger(msg=f"[{__class__.__name__}] Model Config: {model_config}", color="blue")
        self.set_model_path()
        self.load_model()

    def set_model_path(self):
        """"""
        if self.model_path is not None:
            pass
        else:
            self.model_path = self.model_config.get("model_path")
            self.load_method = self.model_config.get("load_method")

    def _get_user_content(self, messages: List[TypeMessage]) -> str:
        """"""
        question = ""
        user_message = messages[-1]
        if isinstance(user_message, (AudioMessage, ImageMessage)):
            if isinstance(user_message.content, str):
                question = user_message.content
            else:
                for content in user_message.content:
                    if isinstance(content, TextContent):
                        question = content.text
                        break
        else:
            question = user_message.content
        return question

    def load_model(self):
        """"""
        self._logger(msg=f"[{__class__.__name__}] Loading model...", color="blue")
        start_time = time.time()
        self.model, self.tokenizer = self.load_method(self.model_path)
        end_time = time.time()
        self._logger(msg=f"[{__class__.__name__}] Loading Done. Use {end_time - start_time:.2f}s", color="blue")

    def parse_tools_call(self, content: str, usage: CompletionUsage) -> ChatCompletion:
        """"""
        if self.tools_config.tools:
            parse_function_call = ParseFunctionCall(content=content, tools=self.tools_config.tools)
            chat_completion_message = parse_function_call.to_chat_completion_message()
            if chat_completion_message.content is None and chat_completion_message.tool_calls:
                finish_reason = "tool_calls"
            else:
                finish_reason = "stop"
        else:
            chat_completion_message = ChatCompletionMessage(role="assistant", content=content)
            finish_reason = "stop"

        choice = ChatChoice(finish_reason=finish_reason, index=0, message=chat_completion_message)
        chat_completion = ChatCompletion(
            id=generate_id(prefix="chat", k=16), created=int(time.time()), model=self.model_name,
            choices=[choice], usage=usage,
        )
        return chat_completion

    def parse_stream_tools_call(self, content: str, _id: str, usage: CompletionUsage) -> ChatCompletionChunk:
        """"""
        if self.tools_config.tools:
            parse_function_call = ParseFunctionCall(content=content, tools=self.tools_config.tools)
            choice_delta = parse_function_call.to_stream_completion_delta()
            if choice_delta.content is None and choice_delta.tool_calls:
                finish_reason = "tool_calls"
            else:
                finish_reason = "stop"
        else:
            choice_delta = ChoiceDelta(role="assistant", content="")
            finish_reason = "stop"

        chunk_choice = ChunkChoice(finish_reason=finish_reason, index=0, delta=choice_delta)
        chat_completion_chunk = ChatCompletionChunk(
            id=_id, created=int(time.time()), model=self.model_name, choices=[chunk_choice],
            usage=usage,
        )
        return chat_completion_chunk

    def _start_logger(self, messages: List[TypeMessage]) -> None:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] User Question: {self._get_user_content(messages=messages)}",
                     color="green")

    def completion(self, messages: List[TypeMessage]) -> ChatCompletion:
        """"""
        self._start_logger(messages=messages)
        completion_function = self.model_config.inference_method.base
        self._logger(msg=f"[{__class__.__name__}] Completion Function: {completion_function}", color="green")
        start = time.time()
        if completion_function is None:
            content = f"Not find completion method: {self.model_name}"
            usage = None
        else:
            content, usage = completion_function(
                model=self.model, tokenizer=self.tokenizer, messages=messages,
                generate_config=self.generate_config, validate=True,
                tools=self.tools_config.tools, tool_choice=self.tools_config.tool_choice
            )
        end = time.time()
        self._logger(msg=f"[{__class__.__name__}] Generating Done. Use {end - start:.2f}s", color="green")
        self._logger(msg=f"[{__class__.__name__}] Completion content: {content}", color="green")
        chat_completion = self.parse_tools_call(content=content, usage=usage)
        return chat_completion

    async def stream_completion(self, messages: List[TypeMessage]) -> Iterable[str]:
        """"""
        self._start_logger(messages=messages)
        _id = generate_id(prefix="chunk-chat", k=16)
        try:
            completion_function = self.model_config.inference_method.stream
            self._logger(msg=f"[{__class__.__name__}] Completion Function: {completion_function}", color="green")
            start = time.time()
            if completion_function is None:
                streamer = None
                content = f"Not find stream completion method: {self.model_name}"
                chunk = stream_message_chunk(content=content, finish_reason="stop", model=self.model_name, _id=_id)
                yield chunk
            else:
                kwargs = dict()
                if self.tools_config is not None:
                    kwargs.update({
                        "tools": self.tools_config.tools,
                        "tool_choice": self.tools_config.tool_choice,
                    })
                streamer = completion_function(
                    model=self.model, tokenizer=self.tokenizer,
                    messages=messages, generate_config=self.generate_config,
                    validate=True, **kwargs
                )

            if streamer is not None:
                answer = ""
                usage = None
                for delta_content, usage in streamer:
                    chunk = stream_message_chunk(
                        content=delta_content, finish_reason=None, model=self.model_name, _id=_id, usage=usage
                    )
                    answer += delta_content
                    yield f"data: {chunk.model_dump_json()}\n\n"
                chunk = self.parse_stream_tools_call(content=answer, _id=_id, usage=usage)
                yield f"data: {chunk.model_dump_json()}\n\n"
                self._logger(msg=f"[{__class__.__name__}] Completion content: {answer}", color="green")
            end = time.time()
            self._logger(msg=f"[{__class__.__name__}] Generating Done. Use {end - start:.2f}s", color="green")

        except Exception as error:
            chunk = stream_message_chunk(
                content=f'Inference ERROR: {error}.', finish_reason="stop", model=self.model_name, _id=_id)
            yield f"data: {chunk.model_dump_json()}\n\n"
            self._logger(msg=f"[{__class__.__name__}] Inference ERROR: {error}.", color="red")
