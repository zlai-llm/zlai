from functools import lru_cache
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer


__all__ = [
    "load_qwen2",
    "load_embedding",
    "load_method_mapping",
]


@lru_cache()
def load_qwen2(model_path: str):
    """"""
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=model_path,
        torch_dtype="auto",
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer


@lru_cache()
def load_embedding(model_path: str):
    """"""
    model = SentenceTransformer(model_path)
    return model


load_method_mapping = {
    "load_qwen2": load_qwen2,
    "load_embedding": load_embedding,
}
