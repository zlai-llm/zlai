import torch
from typing import Any, Dict, Tuple, Optional
from cachetools import cached, LRUCache
from transformers import AutoModelForCausalLM, AutoTokenizer
from zlai.models.utils import get_device_max_memory
from zlai.models.load.cache import *


__all__ = [
    "load_qwen2",
    "load_qwen2_audio",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_qwen2(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """

    :param model_path:
    :param max_memory:
    :return:
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    max_memory = get_device_max_memory(max_memory)
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=model_path,
        torch_dtype="auto",
        device_map="auto",
        max_memory=max_memory,
    ).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_qwen2_audio(
        model_path: str,
        max_memory: Optional[Dict] = None
) -> Tuple[Any, Any]:
    """"""
    from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor
    # max_memory = get_device_max_memory(max_memory)
    processor = AutoProcessor.from_pretrained(model_path)
    model = Qwen2AudioForConditionalGeneration.from_pretrained(
        model_path, device_map="auto",
    ).cuda()
    return model, processor
