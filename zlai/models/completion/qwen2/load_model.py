from typing import Any, Dict, Tuple, Optional
from cachetools import cached, TTLCache
from transformers import AutoModelForCausalLM, AutoTokenizer
from zlai.models.utils import get_device_max_memory
from zlai.models.config import cache_config


__all__ = [
    "load_qwen2",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_qwen2(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=model_path,
        torch_dtype="auto",
        device_map="auto",
        max_memory=max_memory,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer
