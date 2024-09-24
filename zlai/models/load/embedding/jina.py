import torch
from cachetools import cached, LRUCache
from transformers import AutoModel, AutoTokenizer
from ..cache import *


__all__ = [
    "load_jina_embedding_v3",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_jina_embedding_v3(model_path: str):
    """"""
    model = AutoModel.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True,
        use_flash_attn=False,
    )
    if torch.cuda.is_available():
        model = model.to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_path)
    return model, tokenizer
