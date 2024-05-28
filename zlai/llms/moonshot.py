from typing import Optional, List, Any, Literal

from ..schema import Message
from .generate import *
from .generate_config.moonshot import TypeMoonShotGenerate


__all__ = [
    "MoonShot"
]


class MoonShot(OpenAICompletion):
    base_url: Optional[str] = "https://api.moonshot.cn/v1"

    def __init__(
            self,
            generate_config: TypeMoonShotGenerate,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "MOONSHOT_API_KEY",
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

