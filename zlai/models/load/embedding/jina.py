import torch
from cachetools import cached, LRUCache
from transformers import AutoModel
from ..cache import *


__all__ = [
    "load_jina_embedding_v3",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_jina_embedding_v3(model_path: str):
    """"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModel.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True
    ).to_device(device)
    return model
