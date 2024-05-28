from pydantic import BaseModel
from typing import List, Dict, Any, Union

__all__ = [
    "Document",
    "RAGDocuments",
    "RetrieverDocuments",
]


class Document(BaseModel):
    """"""
    content: str
    score: float


class RAGDocuments(BaseModel):
    """"""
    document: str
    vector: List[float]
    metadata: Dict[str, Any]


class RetrieverDocuments(BaseModel):
    """"""
    document: str
    metadata: Dict[str, Any]
    score: float
