import os
from typing import Any, List, Literal, Optional
from zlai.types.messages import TypeMessage
from zlai.types.generate_config.completion import GenerateConfig
from .generate import OpenAICompletion


__all__ = ["LocalCompletion"]


class LocalCompletion(OpenAICompletion):
    base_url: Optional[str] = os.getenv("BASE_URL")

    def __init__(
            self,
            generate_config: Optional[GenerateConfig] = None,
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
        self.messages = messages
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self._create_client()
