from typing import List
from pydantic import BaseModel


__all__ = [
    "DropModelRequest"
]


class DropModelRequest(BaseModel):
    """"""
    method: List[str] = []
    path: List[str] = []
