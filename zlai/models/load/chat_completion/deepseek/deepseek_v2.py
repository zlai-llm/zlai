import torch
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, TTLCache
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from zlai.models.utils import get_device_max_memory
from zlai.models.load.cache import *


__all__ = [
    "load_deepseek_v2",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_deepseek_v2(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, trust_remote_code=True, torch_dtype=torch.bfloat16,
        max_memory=max_memory,
    ).cuda()
    model.generation_config = GenerationConfig.from_pretrained(model_path)
    model.generation_config.pad_token_id = model.generation_config.eos_token_id
    return model, tokenizer
