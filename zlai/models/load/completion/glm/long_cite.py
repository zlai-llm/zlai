import torch
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, LRUCache
from transformers import AutoModelForCausalLM, AutoTokenizer
from zlai.models.utils import get_device_max_memory
from zlai.models.load.cache import *


__all__ = [
    "load_long_cite_glm4",
    "load_long_cite_llama3",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_long_cite_glm4(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, trust_remote_code=True,
        max_memory=max_memory
    ).cuda().eval()
    return model, tokenizer


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_long_cite_llama3(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, trust_remote_code=True,
        max_memory=max_memory
    ).cuda().eval()
    return model, tokenizer