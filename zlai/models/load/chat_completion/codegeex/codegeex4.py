import torch
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, TTLCache
from transformers import AutoModelForCausalLM, AutoTokenizer
from zlai.models.utils import get_device_max_memory
from zlai.models.load.cache import *


__all__ = [
    "load_codegeex4",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_codegeex4(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, trust_remote_code=True,
        max_memory=max_memory
    ).to("cuda").eval()
    return model, tokenizer


