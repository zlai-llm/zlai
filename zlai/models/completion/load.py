import torch
from typing import Any, Dict, Tuple, Optional
from functools import lru_cache
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer


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


@lru_cache()
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


@lru_cache()
def load_embedding(model_path: str):
    """"""
    model = SentenceTransformer(model_path)
    return model


load_method_mapping = {
    "load_qwen2": load_qwen2,
    "load_glm4": load_glm4,
    "load_embedding": load_embedding,
}
