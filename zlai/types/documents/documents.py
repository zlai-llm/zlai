from PIL.Image import Image as TypeImage
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


__all__ = [
    "Document",
    "VectoredDocument",
]


class Document(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Class for storing a piece of text and associated metadata."""

    page_content: Optional[str] = Field(default=None)
    """String text."""
    page_images: Optional[List[TypeImage]] = Field(default_factory=list)
    metadata: Optional[dict] = Field(default_factory=dict)
    """Arbitrary metadata about the page content (e.g., source, relationships to other
        documents, etc.).
    """

    def __init__(self, page_content: Optional[str] = None, **kwargs: Any) -> None:
        """Pass page_content in as positional or named arg."""
        super().__init__(page_content=page_content, **kwargs)


class VectoredDocument(Document):
    """"""
    vector: Optional[List[float]] = None
