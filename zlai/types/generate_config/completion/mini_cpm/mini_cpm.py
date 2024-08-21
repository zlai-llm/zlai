from typing import Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeMiniCPMGenerate",
    "MiniCPMV26GenerateConfig",
]


class MiniCPMV26GenerateConfig(GenerateConfig):
    """"""
    max_new_tokens: int = 2048


TypeMiniCPMGenerate = Union[
    MiniCPMV26GenerateConfig
]
