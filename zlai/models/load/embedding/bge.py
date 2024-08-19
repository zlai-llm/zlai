from cachetools import cached, TTLCache
from sentence_transformers import SentenceTransformer
from ..cache import *


__all__ = [
    "load_embedding",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_embedding(model_path: str):
    """"""
    model = SentenceTransformer(model_path)
    return model
