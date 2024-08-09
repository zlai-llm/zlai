import torch
from functools import lru_cache
from typing import Any, Dict, Tuple, Optional
from transformers import AutoModel, AutoTokenizer
from zlai.models.utils import get_device_max_memory


__all__ = [
    "load_mini_cpm",
]


@lru_cache()
def load_mini_cpm(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    max_memory = get_device_max_memory(max_memory)
    # sdpa or flash_attention_2, no eager
    model = AutoModel.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True,
        attn_implementation='sdpa', torch_dtype=torch.bfloat16, max_memory=max_memory,
    )
    model = model.eval().cuda()
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path, trust_remote_code=True)
    return model, tokenizer
