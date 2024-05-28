from typing import Any, List, Literal, Optional

from ..schema import *
from .generate import *
from .generate_config import *


__all__ = ["Atom", "Llama3"]


class Atom(OpenAICompletion):
    base_url: Optional[str] = "https://api.atomecho.cn/v1"

    def __init__(
            self,
            generate_config: TypeAtomGenerate,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "ATOM_API_KEY",
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


class Llama3(Atom):
    """"""
    def __init__(
            self,
            generate_config: TypeAtomGenerate,
            *args: Any,
            **kwargs: Any
    ):
        """"""
        super().__init__(generate_config=generate_config, *args, **kwargs)
