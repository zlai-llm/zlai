import torch
from functools import lru_cache
from diffusers import KolorsPipeline
from typing import Optional, Dict


__all__ = [
    "load_kolors_diffusers"
]


@lru_cache()
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
