from typing import List, Union
from pydantic import BaseModel


__all__ = [
    "DropModelRequest",
    "GPUMemoryRequest",
]


class DropModelRequest(BaseModel):
    """"""
    model_name: Union[str, List[str]]


class GPUMemoryRequest(BaseModel):
    """"""
    device: Union[int, List[int]]
