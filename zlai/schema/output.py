from pydantic import BaseModel
from typing import List, Literal, Optional


__all__ = [
    "EmbeddingMatchOutput"
]


class EmbeddingMatchOutput(BaseModel):
    """"""
    src: str
    dst: Optional[List[str]] = None
    score: Optional[List[float]] = None
    match_type: Optional[List[Literal["score", "keyword"]]] = ["score"]
    keyword_method: Optional[Literal["content", "keyword"]] = None
    target: Optional[List[str]] = None
