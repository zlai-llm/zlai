from transformers import AutoModel, AutoTokenizer
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, LRUCache
from zlai.models.load.cache import *


__all__ = [
    "load_got_ocr",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_got_ocr(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True,
        low_cpu_mem_usage=True, device_map='cuda', use_safetensors=True, pad_token_id=tokenizer.eos_token_id
    ).eval().cuda()
    return model, tokenizer
