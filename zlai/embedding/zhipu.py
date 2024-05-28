import os
from functools import lru_cache
from typing import List, Union, Tuple, Optional, Literal

from .embedding import EmbeddingMixin
from ..schema import EmbeddingsResponded, ZhipuEmbeddingModel, CompletionUsage, Vector
from .embedding_config import TypeZhipuEmbedding


__all__ = [
    "ZhipuEmbedding"
]


class ZhipuEmbedding(EmbeddingMixin):
    """TODO: 现在不支持批量"""
    model_name: Optional[ZhipuEmbeddingModel] = None
    config: Optional[TypeZhipuEmbedding] = None
    max_len: int = 512
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    verbose: bool = False
    batch_size: Optional[int]
    api_key: Optional[str] = None
    api_key_name: Optional[str] = None

    def __init__(
            self,
            model_name: Optional[ZhipuEmbeddingModel] = None,
            config: Optional[TypeZhipuEmbedding] = None,
            max_len: int = 512,
            max_len_error: Literal['split', 'drop', 'error'] = 'split',
            batch_size: Optional[int] = 256,
            api_key: Optional[str] = None,
            api_key_name: Optional[str] = "ZHIPU_API_KEY",
            verbose: bool = False,
            **kwargs
    ):
        """"""
        self.model_name = model_name
        self.config = config
        self.max_len = max_len
        self.max_len_error = max_len_error
        self.batch_size = batch_size
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.verbose = verbose
        self._create_zhipu_client()

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)

    def _create_zhipu_client(self,) -> None:
        """"""
        try:
            from zhipuai import ZhipuAI
        except ModuleNotFoundError:
            raise ModuleNotFoundError("pip install zhipuai")

        if self.api_key:
            self.zhipu_client = ZhipuAI(api_key=self.api_key)
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
            self.zhipu_client = ZhipuAI(api_key=self.api_key)
        else:
            raise ValueError(f"api_key not found, please set api key")

    @classmethod
    def sum_usages(cls, *usages: CompletionUsage):
        """"""
        usage = CompletionUsage()
        for _usage in usages:
            usage.completion_tokens += _usage.completion_tokens
            usage.prompt_tokens += _usage.prompt_tokens
            usage.total_tokens += _usage.total_tokens
        return usage

    def zhipu_embedding(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        """"""
        embedding_response = EmbeddingsResponded()
        text = self.trans_input_text(text=text)
        for i, _input in enumerate(text):
            response = self.zhipu_client.embeddings.create(
                model=self.config.model,
                input=_input,
            )
            embedding_response.object = response.object
            embedding_response.model = response.model
            embedding_response.data.append(Vector(
                index=i, object=response.data[0].object,
                embedding=response.data[0].embedding
            ))
            embedding_response.usage = self.sum_usages(embedding_response.usage, response.usage)
        return embedding_response

    @lru_cache(maxsize=128)
    def embedding(
            self,
            text: Union[str, List[str], Tuple[str, ...]],
    ) -> EmbeddingsResponded:
        """"""
        return self.zhipu_embedding(text=text)
