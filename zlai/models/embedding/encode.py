import time
from logging import Logger
from typing import Any, List, Dict, Union, Callable, Optional
from sentence_transformers import SentenceTransformer
from zlai.utils.mixin import LoggerMixin
from zlai.types.response.embedding import *
from .bge import *


__all__ = [
    "LoadModelEmbedding",
]


class LoadModelEmbedding(LoggerMixin):
    """"""
    model: Any
    model_config: Dict
    load_method: Union[SentenceTransformer, Callable]

    def __init__(
            self,
            model_path: Optional[str] = None,
            model_config: Optional[Dict] = None,
            model_name: Optional[str] = None,
            load_method: Optional[Callable] = SentenceTransformer,
            logger: Optional[Union[Logger, Callable]] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        self.model_path = model_path
        self.model_config = model_config
        self.model_name = model_name
        self.logger = logger
        self.verbose = verbose
        self.load_method = load_method
        self.args = args
        self.kwargs = kwargs
        self.set_model_path()
        self.load_model()
        self.bge_embedding_model = bge_embedding_model

    def set_model_path(self):
        """"""
        if self.model_path is not None:
            pass
        else:
            self.model_path = self.model_config.get("model_path")
            self.load_method = self.model_config.get("load_method")

    def load_model(self):
        """"""
        self._logger(msg=f"[{__class__.__name__}] Loading model...", color="blue")
        start_time = time.time()
        self.model = self.load_method(self.model_path)
        end_time = time.time()
        self._logger(msg=f"[{__class__.__name__}] Loading Done. Use {end_time - start_time:.2f}s", color="blue")

    def _trans_vectors_to_embedding(self, vectors: List[List[float]]) -> List[Embedding]:
        """"""
        return [Embedding(index=i, embedding=vector) for i, vector in enumerate(vectors)]

    def encode(self, text: Union[str, List[str]]) -> CreateEmbeddingResponse:
        """"""
        usage, vectors = Usage(), []
        response = CreateEmbeddingResponse(model=self.model_name, usage=usage, data=vectors)
        if isinstance(text, str):
            text = [text]

        self._logger(msg=f"[{__class__.__name__}] Embedding {len(text)} sentences...", color="green")
        if self.model_name in self.bge_embedding_model:
            vectors, usage = encode(text=text, model=self.model)
            response.data = self._trans_vectors_to_embedding(vectors=vectors)
            response.usage = usage
            self._logger(msg=f"[{__class__.__name__}] Embedding Done.", color="green")
            return response
        else:
            raise NotImplementedError(f"Embedding model {self.model_name} not found.")
