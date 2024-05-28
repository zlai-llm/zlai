try:
    import dashscope
    from dashscope import BatchTextEmbedding
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install dashscope")
import os
from http import HTTPStatus
from functools import lru_cache
from typing import List, Union, Tuple, Optional, Literal, Generator

from ..schema import EmbeddingsResponded, CompletionUsage, Vector
from .embedding import EmbeddingMixin
from .embedding_config import *


__all__ = [
    "AliEmbedding"
]


class AliEmbedding(EmbeddingMixin):
    """"""
    config: Optional[TypeAliEmbedding] = None
    max_len: int = 512
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    verbose: bool = False
    batch_size: Optional[int]
    api_key: Optional[str] = None
    api_key_name: Optional[str] = None

    def __init__(
            self,
            config: Optional[TypeAliEmbedding] = None,
            max_len: int = 512,
            max_len_error: Literal['split', 'drop', 'error'] = 'split',
            batch_size: Optional[int] = 25,
            api_key: Optional[str] = None,
            api_key_name: Optional[str] = "ALI_API_KEY",
            verbose: bool = False,
            **kwargs
    ):
        """"""
        self.config = config
        self.max_len = max_len
        self.max_len_error = max_len_error
        self.batch_size = batch_size
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.verbose = verbose
        self._create_ali_client()

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)

    def _create_ali_client(self, ) -> None:
        """"""
        if self.api_key:
            dashscope.api_key = self.api_key
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
            dashscope.api_key = self.api_key
        else:
            raise ValueError(f"api_key not found, please set api key")

        self.ali_client = dashscope.TextEmbedding

    @classmethod
    def sum_usages(cls, *usages: CompletionUsage):
        """"""
        usage = CompletionUsage()
        for _usage in usages:
            usage.completion_tokens += _usage.completion_tokens
            usage.prompt_tokens += _usage.prompt_tokens
            usage.total_tokens += _usage.total_tokens
        return usage

    @classmethod
    def _batched(cls, inputs: List, batch_size: int) -> Generator[List, None, None]:
        for i in range(0, len(inputs), batch_size):
            yield inputs[i:i + batch_size]

    def ali_embedding(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        """"""
        if self.batch_size > 25:
            raise ValueError("batch_size cannot be greater than 25.")

        embedding_response = EmbeddingsResponded(model=self.config.model)
        text = self.trans_input_text(text=text)
        for i, _input in enumerate(self._batched(inputs=text, batch_size=self.batch_size)):
            response = self.ali_client.call(
                model=self.config.model,
                input=_input,
            )
            if response.status_code == HTTPStatus.OK:
                vectors = [Vector(embedding=emb.get("embedding", []), index=i * self.batch_size + emb.get("text_index")) for emb in response.output['embeddings']]
                embedding_response.data.extend(vectors)
                embedding_response.usage = self.sum_usages(embedding_response.usage, CompletionUsage(**response.usage))
            else:
                raise ValueError(f"Ali embedding error: {response.status_code}. Message: {response.message}")
        return embedding_response

    @lru_cache(maxsize=128)
    def embedding(
            self,
            text: Union[str, List[str], Tuple[str, ...]],
    ) -> EmbeddingsResponded:
        """"""
        return self.ali_embedding(text=text)
