import time
from logging import Logger
from typing import Any, List, Dict, Iterable, Optional, Callable

from zlai.types import *
from zlai.types.chat_completion import Choice as ChatChoice
from zlai.types.chat_completion_chunk import Choice as ChunkChoice
from zlai.utils.mixin import LoggerMixin
from ..types import *
from ..utils import *
from .load import *
from .glm4 import *
from .qwen2 import *


__all__ = [
    "LoadModelCompletion",
]


class LoadModelCompletion(LoggerMixin):
    """"""
    model: Any
    tokenizer: Any
    model_config: Dict
    load_method: str

    def __init__(
            self,
            model_path: Optional[str] = None,
            models_config: Optional[List[Dict]] = None,
            model_name: Optional[str] = None,
            generate_config: Optional[TypeInferenceGenerateConfig] = None,
            tools_config: Optional[ToolsConfig] = None,
            load_method: Optional[str] = "auto",
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        self.model_path = model_path
        self.models_config = models_config
        self.model_name = model_name
        self.generate_config = generate_config
        self.tools_config = tools_config
        self.logger = logger
        self.verbose = verbose
        self.load_method = load_method
        self.args = args
        self.kwargs = kwargs
        self.set_model_path()
        self.load_model()
        self.qwen_2_completion_model: List[str] = [
            "Qwen2-0.5B-Instruct",
            "Qwen2-1.5B-Instruct",
            "Qwen2-7B-Instruct",
            "Qwen2-57B-A14B-Instruct-GPTQ-Int4",
        ]
        self.glm_4_completion_model: List[str] = [
            "glm-4-9b-chat",
            "glm-4-9b-chat-1m",
            "glm-4v-9b",
        ]

    def set_model_path(self):
        """"""
        if self.model_path is not None:
            pass
        else:
            self.model_config = self.get_model_config(model_name=self.model_name, models_config=self.models_config)
            self.model_path = self.model_config.get("model_path")
            self.load_method = self.model_config.get("load_method")

    def _get_user_content(self, messages: List[TypeMessage]) -> str:
        """"""
        user_message = messages[-1]
        if isinstance(user_message, ImageMessage):
            user_message.split_image()
        return user_message.content

    def load_model(self):
        """"""
        self._logger(msg=f"[{__class__.__name__}] Loading model...", color="blue")
        start_time = time.time()
        model_attr = load_method_mapping.get(self.load_method)(self.model_path)
        if isinstance(model_attr, tuple):
            self.model, self.tokenizer = model_attr
        else:
            self.model = model_attr
        end_time = time.time()
        self._logger(msg=f"[{__class__.__name__}] Loading Done. Use {end_time - start_time:.2f}s", color="blue")

    def get_model_config(
            self,
            model_name: str,
            models_config: List[Dict],
    ) -> Dict:
        """"""
        for config in models_config:
            if config["model_name"] == model_name:
                return config
        raise ValueError(f"Model {model_name} not found.")

    def text_encode(self, text: List[str]) -> List[List[float]]:
        """"""
        vectors = self.model.encode(text, normalize_embeddings=True).to_list()
        return vectors

    def parse_tools_call(self, content: str) -> ChatCompletion:
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
            id=generate_id(prefix="chat", k=16), created=int(time.time()), model=self.model_name, choices=[choice]
        )
        return chat_completion

    def parse_stream_tools_call(self, content: str, _id: str) -> ChatCompletionChunk:
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
            id=_id, created=int(time.time()), model=self.model_name, choices=[chunk_choice]
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
        if self.model_name in self.qwen_2_completion_model:
            content = completion_qwen_2(
                model=self.model, tokenizer=self.tokenizer, messages=messages,
                generate_config=self.generate_config,
            )
        elif self.model_name in self.glm_4_completion_model:
            content = completion_glm_4(
                model=self.model, tokenizer=self.tokenizer, messages=messages,
                generate_config=self.generate_config, validate=True,
                tools=self.tools_config.tools, tool_choice=self.tools_config.tool_choice)
        else:
            content = f"Not find completion method: {self.model_name}"

        self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")
        self._logger(msg=f"[{__class__.__name__}] Completion content: {content}", color="green")

        chat_completion = self.parse_tools_call(content=content)
        return chat_completion

    async def stream_completion(self, messages: List[TypeMessage]) -> Iterable[str]:
        """"""
        self._start_logger(messages=messages)
        _id = generate_id(prefix="chunk-chat", k=16)
        try:
            if self.model_name in self.qwen_2_completion_model:
                streamer = stream_completion_qwen_2(
                        model=self.model, tokenizer=self.tokenizer,
                        messages=messages, generate_config=self.generate_config,
                )
            elif self.model_name in self.glm_4_completion_model:
                streamer = stream_completion_glm_4(
                        model=self.model, tokenizer=self.tokenizer,
                        messages=messages, generate_config=self.generate_config,
                        validate=True, tools=self.tools_config.tools,
                        tool_choice=self.tools_config.tool_choice,
                )
            else:
                streamer = None
                content = f"Not find stream completion method: {self.model_name}"
                chunk = stream_message_chunk(content=content, finish_reason="stop", model=self.model_name, _id=_id)
                yield chunk

            if streamer is not None:
                answer = ""
                for delta_content in streamer:
                    chunk = stream_message_chunk(
                        content=delta_content, finish_reason=None, model=self.model_name, _id=_id)
                    answer += delta_content
                    yield f"data: {chunk.model_dump_json()}\n\n"
                chunk = self.parse_stream_tools_call(content=answer, _id=_id)
                yield f"data: {chunk.model_dump_json()}\n\n"
                self._logger(msg=f"[{__class__.__name__}] Completion content: {answer}", color="green")

            self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")

        except Exception as error:
            chunk = stream_message_chunk(
                content=f'Inference ERROR: {error}.', finish_reason="stop", model=self.model_name, _id=_id)
            yield f"data: {chunk.model_dump_json()}\n\n"
            self._logger(msg=f"[{__class__.__name__}] Inference ERROR: {error}.", color="red")
