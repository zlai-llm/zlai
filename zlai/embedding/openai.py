import os
from functools import lru_cache
from typing import List, Union, Tuple, Optional, Literal
from openai import OpenAI

from zlai.types.response.embedding import CreateEmbeddingResponse
from .embedding import EmbeddingMixin
from .embedding_config import TypeOpenAIEmbedding


__all__ = [
    "OpenAIEmbedding"
]


class OpenAIEmbedding(EmbeddingMixin):
    """"""
    config: Optional[TypeOpenAIEmbedding] = None
    max_len: int = 512
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    verbose: bool = False
    batch_size: Optional[int]
    api_key: Optional[str] = None
    api_key_name: Optional[str] = None

    def __init__(
            self,
            config: Optional[TypeOpenAIEmbedding] = None,
            max_len: int = 8000,
            max_len_error: Literal['split', 'drop', 'error'] = 'split',
            batch_size: Optional[int] = 256,
            base_url: Optional[str] = os.getenv("BASE_URL", "http://localhost:8000/"),
            api_key: Optional[str] = "BASE_URL",
            api_key_name: Optional[str] = "BASE_URL",
            timeout: Optional[float] = 30.0,
            max_retries: Optional[int] = 5,
            verbose: bool = False,
            **kwargs
    ):
        """"""
        self.config = config
        self.max_len = max_len
        self.max_len_error = max_len_error
        self.batch_size = batch_size
        self.base_url = base_url
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.timeout = timeout
        self.max_retries = max_retries
        self.verbose = verbose
        self._create_client()
        self.kwargs = kwargs

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> CreateEmbeddingResponse:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)

    def _create_client(self,) -> None:
        """"""
        if self.api_key:
            self.client = OpenAI(
                base_url=self.base_url, api_key=self.api_key,
                timeout=self.timeout, max_retries=self.max_retries)
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
            self.client = OpenAI(
                base_url=self.base_url, api_key=self.api_key,
                timeout=self.timeout, max_retries=self.max_retries)
        else:
            raise ValueError(f"api_key not found, please set api key")

    def openai_embedding(
            self,
            text: Union[str, List[str]],
    ) -> CreateEmbeddingResponse:
        """"""
        text = self.trans_input_text(text=text)
        response = self.client.embeddings.create(
            model=self.config.model,
            input=text,
        )
        return CreateEmbeddingResponse.model_validate(response.model_dump())

    @lru_cache(maxsize=128)
    def embedding(
            self,
            text: Union[str, List[str], Tuple[str, ...]],
    ) -> CreateEmbeddingResponse:
        """"""
        return self.openai_embedding(text=text)
