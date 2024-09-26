from typing import Any, List, Literal, Optional

from ..schema import *
from .generate import *
from zlai.llms.generate_config.api.openai import TypeOpenAIGenerate

__all__ = ["OpenAI"]


class OpenAI(OpenAICompletion):
    base_url: Optional[str] = "https://api.openai.com/v1"

    def __init__(
            self,
            generate_config: Optional[TypeOpenAIGenerate] = None,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "OPENAI_API_KEY",
            base_url: Optional[str] = None,
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
