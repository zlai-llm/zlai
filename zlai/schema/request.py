from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from .url import Model
from .messages import Message
from .response import CompletionMessage
from ..llms.generate_config import *


__all__ = [
    "GenerateConfig",
    "BaseGenerateConfig",
    "EmbeddingRequest",
]


class EmbeddingRequest(BaseModel):
    """"""
    model: str = "bge-small"
    input: List[str] = ["你好"]
    instruction: bool = False
