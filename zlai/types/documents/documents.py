from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field


__all__ = [
    "Document",
    "VectoredDocument",
]


class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""

    page_content: str
    """String text."""
    metadata: dict = Field(default_factory=dict)
    """Arbitrary metadata about the page content (e.g., source, relationships to other
        documents, etc.).
    """

    def __init__(self, page_content: str, **kwargs: Any) -> None:
        """Pass page_content in as positional or named arg."""
        super().__init__(page_content=page_content, **kwargs)


class VectoredDocument(Document):
    """"""
    vector: Optional[List[float]] = None
