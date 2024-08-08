import torch
from typing import Dict, Optional
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from .glm4 import load_glm4
from .qwen2 import load_qwen2
from .mini_cpm import load_mini_cpm


__all__ = [
    "load_qwen2",
    "load_glm4",
    "load_embedding",
    "load_method_mapping",
    "get_device_max_memory",
]


def get_device_max_memory(max_memory: Optional[Dict] = None) -> Dict:
    """"""
    if max_memory is None and torch.cuda.is_available():
        max_memory = {0: "20GB"}
    else:
        max_memory = None
    return max_memory


@lru_cache()
def load_embedding(model_path: str):
    """"""
    model = SentenceTransformer(model_path)
    return model


load_method_mapping = {
    "load_qwen2": load_qwen2,
    "load_glm4": load_glm4,
    "load_mini_cpm": load_mini_cpm,
    "load_embedding": load_embedding,
}
