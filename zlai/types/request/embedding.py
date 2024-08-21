from typing import List, Union
from .base import BaseRequest


__all__ = ["EmbeddingRequest"]


class EmbeddingRequest(BaseRequest):
    """EmbeddingRequest"""

    input: Union[str, List[str]]
    """Input text to embed, encoded as a string or array of tokens. To embed multiple inputs in a single request, 
    pass an array of strings or array of token arrays. The input must not exceed the max input tokens for the 
    model (8192 tokens for text-embedding-ada-002), cannot be an empty string, and any array must be 2048 dimensions 
    or less. Example Python code for counting tokens."""

    model: str
    """ID of the model to use. You can use the List models API to see all of your available models, 
    or see our Model overview for descriptions of them."""

    encoding_format: str = "float"
    """The format to return the embeddings in. Can be either float or base64."""

    dimensions: int = None
    """The number of dimensions the resulting output embeddings should have. 
    Only supported in text-embedding-3 and later models."""

    user: str = None
    """A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse."""
