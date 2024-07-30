import time
from logging import Logger
from threading import Thread
from typing import Any, List, Dict, Union, Optional, Callable
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice, ChatCompletionChunk
from transformers import TextIteratorStreamer

from zlai.llms import GenerateConfig
from zlai.utils.mixin import LoggerMixin
from .load import *
from ..types import *


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

    def completion(self, messages: List[Dict]) -> str:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] User Question: {messages[-1].get('content')}", color="green")
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        content = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
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

    async def stream_completion(self, messages: List[Dict]) -> str:
        """"""
        self._logger(msg=f"[{__class__.__name__}] Generating...", color="green")
        self._logger(msg=f"[{__class__.__name__}] User Question: {messages[-1].get('content')}", color="green")
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
