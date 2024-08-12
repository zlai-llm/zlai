import torch
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, TTLCache
from transformers import AutoModelForCausalLM, AutoTokenizer
from zlai.models.utils import get_device_max_memory
from zlai.models.config import cache_config


__all__ = [
    "load_glm4",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_glm4(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    device = "cuda"
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=model_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        max_memory=max_memory,
    ).to(device).eval()
    return model, tokenizer
