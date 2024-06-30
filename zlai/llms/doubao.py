from typing import Any, List, Literal, Optional

from ..schema import *
from .generate import *
from .generate_config.doubao import TypeDouBaoGenerate


__all__ = ["DouBao"]


class DouBao(OpenAICompletion):
    base_url: Optional[str] = "https://ark.cn-beijing.volces.com/api/v3"

    def __init__(
            self,
            generate_config: Optional[TypeDouBaoGenerate] = None,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "DOUBAO_API_KEY",
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
