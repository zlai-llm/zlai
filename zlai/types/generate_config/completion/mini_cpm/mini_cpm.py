from typing import List, Union, Optional
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeMiniCPMGenerate",
    "MiniCPMV26GenerateConfig",
    "MiniCPM3GenerateConfig",
]


class MiniCPMV26GenerateConfig(GenerateConfig):
    """"""
    max_new_tokens: int = 2048


class MiniCPM3GenerateConfig(GenerateConfig):
    """"""
    max_new_tokens: int = 2048
    do_sample: Optional[bool] = True
    top_p: Optional[float] = 0.8
    temperature: Optional[float] = 0.8
    bos_token_id: Optional[int] = 1
    eos_token_id: Optional[List[int]] = [2, 73440]


TypeMiniCPMGenerate = Union[
    MiniCPMV26GenerateConfig,
    MiniCPM3GenerateConfig,
]
