from typing import Optional
from pydantic import Field, BaseModel


__all__ = [
    "EmbeddingConfig",
]


class EmbeddingConfig(BaseModel):
    """"""
    model: Optional[str] = Field(default=None, description="Embeddings model")
