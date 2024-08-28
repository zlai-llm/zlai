import os
from typing import Any, List, Union, Iterable, Literal, Optional
from zlai.types.messages import TypeMessage
from zlai.types.generate_config.completion import GenerateConfig
from zlai.types.chat import ChatCompletion
from zlai.types.request.completion import ChatCompletionRequest
from .generate import OpenAICompletion
from ..schema import Message


__all__ = ["LocalCompletion"]


class LocalCompletion(OpenAICompletion):
    base_url: Optional[str] = os.getenv("BASE_URL")

    def __init__(
            self,
            generate_config: Optional[GenerateConfig] = None,
            api_key: Optional[str] = "EMPTY",
            messages: Optional[List[TypeMessage]] = None,
            model: Optional[str] = None,
            stream: Optional[bool] = False,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "BASE_URL",
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        super().__init__(
            generate_config=generate_config,
            api_key=api_key,
            api_key_name=api_key_name,
            *args, **kwargs)
        self.messages = messages
        self.model = model
        self.stream = stream
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self._create_client()

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[TypeMessage]] = None,
    ) -> Union[ChatCompletion, Message, Iterable[ChatCompletion], str]:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        messages = [message.to_dict() for message in messages]
        request = ChatCompletionRequest.model_validate({
            **self.generate_config.model_dump(),
            **{"messages": messages, "model": self.model, "stream": self.stream}})
        completion = self.client.chat.completions.create(**request.gen_kwargs())
        return completion
