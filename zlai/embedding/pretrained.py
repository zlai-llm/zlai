from typing import Optional, Callable, Literal, Union, List, Tuple
from functools import lru_cache
from ..schema import EmbeddingsResponded
from .embedding import EmbeddingMixin


__all__ = [
    "PretrainedEmbedding"
]


class PretrainedEmbedding(EmbeddingMixin):
    """"""
    def __init__(
            self,
            model_name: Optional[str] = None,
            model_path: Optional[str] = None,
            batch_size: int = 128,
            max_len: int = 512,
            instruction: bool = False,
            max_len_error: Literal['split', 'drop', 'error'] = 'split',
            normalize_embeddings: bool = False,
            device: Optional[str] = None,
            verbose: bool = False,
            logger: Optional[Callable] = None,
            **kwargs
    ):
        """"""
        self.verbose = verbose
        self.logger = logger

        # local
        self.model_name = model_name
        self.max_len = max_len
        self.instruction = instruction
        self.max_len_error = max_len_error
        self.normalize_embeddings = normalize_embeddings
        self.device = device

        # from pretrained model
        self.model_path = model_path
        self.batch_size = batch_size
        self.pretrained_model = self.from_pretrained()

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)

    @lru_cache()
    def from_pretrained(self):
        """"""
        from sentence_transformers import SentenceTransformer
        if self.model_path:
            self._logger(msg="Loading model ...", color="green")
            model = SentenceTransformer(self.model_path, device=self.device)
            self._logger(msg="Success load model ...", color="green")
            return model
        else:
            raise ValueError(f"Path: {self.model_path} not find.")

    def pretrained_model_embedding(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        """"""
        text = self.trans_input_text(text=text)
        usage = self.tokens_usage(text=text)

        vectors = self.pretrained_model.encode(
            sentences=text, batch_size=self.batch_size, show_progress_bar=self.verbose,
            device=self.device, normalize_embeddings=self.normalize_embeddings,
        ).tolist()

        data = self.trans_vectors(vectors=vectors)
        emb_output = EmbeddingsResponded(object='list', data=data, model=self.model_path, usage=usage)
        return emb_output

    def embedding(
            self,
            text: Union[str, List[str], Tuple[str, ...]],
    ) -> EmbeddingsResponded:
        """"""
        text = self.trans_input_text(text=text)
        return self.pretrained_model_embedding(text=text)
