from typing import List, Literal, Optional
from pydantic import BaseModel, Field


__all__ = [
    "Usage",
    "Embedding",
    "CreateEmbeddingResponse",
]


class Usage(BaseModel):
    prompt_tokens: int = Field(default=0)
    """The number of tokens used by the prompt."""

    total_tokens: int = Field(default=0)
    """The total number of tokens used by the request."""


class Embedding(BaseModel):
    embedding: List[float]
    """The embedding vector, which is a list of floats.

    The length of vector depends on the model as listed in the
    [embedding guide](https://platform.openai.com/docs/guides/embeddings).
    """

    index: int
    """The index of the embedding in the list of embeddings."""

    object: Literal["embedding"] = Field(default="embedding")
    """The object type, which is always "embedding"."""


class CreateEmbeddingResponse(BaseModel):
    data: List[Embedding]
    """The list of embeddings generated by the model."""

    model: str
    """The name of the model used to generate the embedding."""

    object: Optional[Literal["list"]] = Field(default="list")
    """The object type, which is always "list"."""

    usage: Usage
    """The usage information for the request."""
