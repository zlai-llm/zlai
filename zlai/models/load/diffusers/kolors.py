import torch
from cachetools import cached, LRUCache
from diffusers import KolorsPipeline, KolorsImg2ImgPipeline
from typing import Optional, Dict
from ..cache import *


__all__ = [
    "load_kolors_diffusers",
    "load_kolors_image2image",
]


@cached(cache=LRUCache(**cache_config.model_dump()))
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


@cached(cache=LRUCache(**cache_config.model_dump()))
def load_kolors_image2image(
        model_path: str,
        max_memory: Optional[Dict] = None,
):
    pipe = KolorsImg2ImgPipeline.from_pretrained(
        model_path, variant="fp16", torch_dtype=torch.float16,
        max_memory=max_memory,
    ).to("cuda")
    return pipe
