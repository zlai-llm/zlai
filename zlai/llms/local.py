import os
from typing import Any, List, Dict, Union, Iterable, Literal, Optional
from zlai.types.chat import ChatCompletion
from zlai.types.request.completion import ChatCompletionRequest
from zlai.types.messages import TypeMessage, UserMessage
from .generate_config import GenerateConfig
from .generate import OpenAICompletion


__all__ = ["LocalCompletion"]


class LocalCompletion(OpenAICompletion):
    base_url: Optional[str]

    def __init__(
            self,
            generate_config: Optional[GenerateConfig] = None,
            base_url: Optional[str] = os.getenv("BASE_URL", "http://localhost:8000/"),
            api_key: Optional[str] = "EMPTY",
            messages: Optional[List[TypeMessage]] = None,
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
        self.base_url = base_url
        self.messages = messages
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self._create_client()

    @classmethod
    def _make_messages(
            cls,
            query: Optional[str] = None,
            messages: Optional[List[TypeMessage]] = None,
    ) -> List[Dict]:
        """"""
        if messages:
            messages = messages
        elif query:
            messages = [UserMessage(content=query)]
        messages = [message.to_dict() for message in messages]
        return messages

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[TypeMessage]] = None,
    ) -> Union[ChatCompletion, TypeMessage, Iterable[ChatCompletion], str]:
        """"""
        self.generate_config.messages = self._make_messages(query=query, messages=messages)
        request = ChatCompletionRequest.model_validate(self.generate_config.model_dump())
        ChatCompletionRequest.model_rebuild()
        completion = self.client.chat.completions.create(**request.gen_kwargs())
        return completion
