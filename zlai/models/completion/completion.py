import time
from logging import Logger
from threading import Thread
from typing import Any, List, Dict, Union, Optional, Callable
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice, ChatCompletionChunk
from transformers import TextIteratorStreamer

from zlai.types.messages import TypeMessage
from zlai.utils.mixin import LoggerMixin
from ..types import *
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
            generate_config: Optional[StreamInferenceGenerateConfig] = None,
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

    def completion(self, messages: List[TypeMessage]) -> str:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] User Question: {messages[-1].content}", color="green")
        if self.model_name in self.qwen_2_completion_model:
            content = completion_qwen_2(model=self.model, tokenizer=self.tokenizer, messages=messages)
        elif self.model_name in self.glm_4_completion_model:
            content = completion_glm_4(
                model=self.model, tokenizer=self.tokenizer, messages=messages,
                validate=True, tools=self.generate_config.tools,
                tool_choice=self.generate_config.tool_choice)
        else:
            content = f"Not find completion method: {self.model_name}"
        self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")
        self._logger(msg=f"[{__class__.__name__}] Completion content: {content}", color="green")
        return content

    def _get_chunk(self, _id: int, choice: Choice) -> ChatCompletionChunk:
        """"""
        chunk = ChatCompletionChunk(
            id=str(_id), object="chat.completion.chunk", created=int(time.time()),
            model="blah", choices=[choice],
        )
        return chunk

    async def stream_completion(self, messages: List[TypeMessage]) -> str:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] User Question: {messages[-1].content}", color="green")
        try:
            streamer = TextIteratorStreamer(self.tokenizer)
            inputs = self.tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, return_tensors="pt").to(self.model.device)

            gen_config = {
                "inputs": inputs, "streamer": streamer,
                **self.generate_config.stream_generate_config(),
            }
            thread = Thread(target=self.model.generate, kwargs=gen_config)
            thread.start()
            answer = ""
            for i, response in enumerate(streamer):
                if i > 0:
                    content = response.replace(self.tokenizer.eos_token, '')
                    answer += content
                    choice = Choice(index=0, finish_reason=None, delta=ChoiceDelta(content=content))
                    chunk = self._get_chunk(i - 1, choice)
                    yield f"data: {chunk.model_dump_json()}\n\n"

            choice = Choice(index=0, finish_reason="stop", delta=ChoiceDelta(content=""))
            chunk = self._get_chunk(i, choice)
            yield f"data: {chunk.model_dump_json()}\n\n"
            self._logger(msg=f"[{__class__.__name__}] Generating Done.", color="green")
            self._logger(msg=f"[{__class__.__name__}] Completion content: {answer}", color="green")
        except Exception as error:
            choice = Choice(index=0, finish_reason="stop", delta=ChoiceDelta(content=f'Inference ERROR: {error}.'))
            chunk = self._get_chunk(i, choice)
            yield f"data: {chunk.model_dump_json()}\n\n"
            self._logger(msg=f"[{__class__.__name__}] Inference ERROR: {error}.", color="red")
