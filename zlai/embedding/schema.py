import numpy as np
from typing import List, Optional
from pydantic import BaseModel, Field
from ..schema import CompletionUsage


__all__ = [
    "CompletionUsage",
    "EmbeddingRequest",
    "EmbeddingsResponded",
    "Vector",
]


class EmbeddingRequest(BaseModel):
    """"""
    model: str = "bge-small"
    input: List[str] = ["你好"]
    instruction: bool = False


class Vector(BaseModel):
    object: str = Field(default="list", description="")
    index: Optional[int] = Field(default=0, description="")
    embedding: List[float] = Field(default=[], description="")


class EmbeddingsResponded(BaseModel):
    object: str = Field(default="list", description="")
    data: List[Vector] = Field(default=[], description="")
    model: str = Field(default="embedding-2", description="")
    usage: CompletionUsage = Field(default=CompletionUsage(), description="")

    def to_numpy(self) -> np.ndarray:
        """"""
        vectors = [vec.embedding for vec in self.data]
        return np.array(vectors)

    def to_list(self) -> List[List[float]]:
        vectors = [vec.embedding for vec in self.data]
        return vectors
