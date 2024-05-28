from typing import Any, Union, List, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

from .url import Model
from .messages import Message
from .response import CompletionMessage
from ..llms.generate_config import TypeLocalGenerate, TypeZhipuGenerate, TypeAliGenerate, GenerateConfig, BaseGenerateConfig

__all__ = [
    "LLMRequest",
    "GenerateConfig",
    "BaseGenerateConfig",
    "EmbeddingRequest",
]

TypeGenerateConfig = Union[GenerateConfig, BaseGenerateConfig, TypeLocalGenerate, TypeZhipuGenerate, TypeAliGenerate]


class LLMRequest(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: Optional[Union[Model, str]] = ''
    messages: Optional[List[Message]] = [CompletionMessage(content='hi.', role='user')]
    generate_config: Optional[TypeGenerateConfig]


class EmbeddingRequest(BaseModel):
    """"""
    model: str = "bge-small"
    input: List[str] = ["你好"]
    instruction: bool = False
