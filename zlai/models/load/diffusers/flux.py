import torch
from cachetools import cached, TTLCache
from diffusers import FluxPipeline
from typing import Optional, Dict
from ..cache import *


__all__ = [
    "load_flux_diffusers"
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_flux_diffusers(
    model_path: str,
    max_memory: Optional[Dict] = None,
):
    """Load the Kolors Diffusers model."""
    pipe = FluxPipeline.from_pretrained(
        model_path, torch_dtype=torch.bfloat16,
        max_memory=max_memory,
    ).to("cuda")
    return pipe
