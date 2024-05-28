from typing import *
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel

__all__ = [
    "LocalModel",
    "ParseInfo",
]


@dataclass
class LocalModel(str, Enum):
    """"""
    chatglm3_6b: str = "chatglm3-6b"
    chatglm3_6b_32k: str = "chatglm3-6b-32k"


class ParseInfo(BaseModel):
    """"""
    content: str = ''
    parsed_data: List = []
    error_message: Optional[str] = None

