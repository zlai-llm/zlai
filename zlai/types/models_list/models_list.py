from typing import Literal, Optional
from pydantic import BaseModel, Field


__all__ = [
    "Model",
]


class Model(BaseModel):
    id: str = Field(description="""The model identifier, which can be referenced in the API endpoints.""")
    created: Optional[int] = Field(default=None, description="""The Unix timestamp (in seconds) when the model was created.""")
    object: Literal["model"] = Field(default="model", description="""The object type, which is always "model".""")
    owned_by: Optional[str] = Field(default="Open Source", description="""The organization that owns the model.""")
