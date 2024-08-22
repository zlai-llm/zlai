from typing import List, Union
from pydantic import BaseModel


__all__ = [
    "DropModelRequest"
]


class DropModelRequest(BaseModel):
    """"""
    model_name: Union[str, List[str]]
