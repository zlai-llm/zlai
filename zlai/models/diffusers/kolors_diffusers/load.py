import torch
from cachetools import cached, TTLCache
from diffusers import KolorsPipeline
from typing import Optional, Dict
from zlai.models.config import cache_config


__all__ = [
    "load_kolors_diffusers"
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_kolors_diffusers(
    model_path: str,
    max_memory: Optional[Dict] = None,
):
    """Load the Kolors Diffusers model."""
    pipe = KolorsPipeline.from_pretrained(
        model_path, torch_dtype=torch.float16, variant="fp16",
        max_memory=max_memory,
    ).to("cuda")
    return pipe
