from typing import *
from pydantic import BaseModel


__all__ = [
    "ParseInfo",
]


class ParseInfo(BaseModel):
    """"""
    content: str = ''
    parsed_data: List = []
    error_message: Optional[str] = None
