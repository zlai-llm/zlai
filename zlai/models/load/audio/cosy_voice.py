from cachetools import cached, TTLCache
from typing import Any
from zlai.models.tts.cosy_voice.cosyvoice.cli.cosyvoice import CosyVoice
from ..cache import *


__all__ = [
    "load_cosy_voice",
]


@cached(cache=TTLCache(**cache_config.model_dump()))
def load_cosy_voice(
    model_path: str,
    **kwargs: Any,
) -> CosyVoice:
    """Load a Cosy Voice model."""
    cosy_voice = CosyVoice(model_path)
    return cosy_voice
