from typing import List, Union
from pydantic import BaseModel, ConfigDict


__all__ = [
    "DropModelRequest",
    "GPUMemoryRequest",
]


class DropModelRequest(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: Union[str, List[str]]


class GPUMemoryRequest(BaseModel):
    """"""
    device: Union[int, List[int]]
