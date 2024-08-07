from pydantic import BaseModel
from typing import Optional, Literal


__all__ = [
    "MarkdownLine",
]


class MarkdownMetadata(BaseModel):
    """"""
    type: Optional[Literal["title", "table", "li", "content"]] = None
    level: Optional[int] = None
    src: Optional[str] = None


class MarkdownLine(MarkdownMetadata):
    """"""
    origin: Optional[str] = None
    content: Optional[str] = None
