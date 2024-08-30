from typing import Any, Dict, Tuple, Optional
from cachetools import cached, LRUCache
from zlai.models.load.cache import *


__all__ = [
    "load_qwen2_vl",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_qwen2_vl(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_path, torch_dtype="auto", device_map="auto"
    ).cuda()
    processor = AutoProcessor.from_pretrained(model_path)
    return model, processor
