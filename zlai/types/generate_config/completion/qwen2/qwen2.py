from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeQwen2Generate",
    "Qwen2GenerateConfig",
    "Qwen2Instruct05BGenerateConfig",
    "Qwen2Instruct15BGenerateConfig",
    "Qwen2Instruct7BGenerateConfig",
    "Qwen2Audio7BInstructGenerateConfig",
]


class Qwen2GenerateConfig(GenerateConfig):
    max_new_tokens: Optional[int] = 512
    top_k: Optional[int] = 20
    top_p: Optional[float] = 0.8
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.7
    repetition_penalty: Optional[float] = 1.05


class Qwen2Instruct05BGenerateConfig(Qwen2GenerateConfig):
    repetition_penalty: Optional[float] = 1.1


class Qwen2Instruct15BGenerateConfig(Qwen2GenerateConfig):
    repetition_penalty: Optional[float] = 1.1


class Qwen2Instruct7BGenerateConfig(Qwen2GenerateConfig):
    repetition_penalty: Optional[float] = 1.1


class Qwen2Audio7BInstructGenerateConfig(GenerateConfig):
    """"""
    repetition_penalty: Optional[float] = 1.1
    do_sample: Optional[bool] = True
    max_length: int = 256
    top_k: Optional[int] = 20
    top_p: Optional[float] = 0.5
    temperature: Optional[float] = 0.7


TypeQwen2Generate = Union[
    Qwen2GenerateConfig,
    Qwen2Instruct05BGenerateConfig,
    Qwen2Instruct15BGenerateConfig,
    Qwen2Instruct7BGenerateConfig,
    Qwen2Audio7BInstructGenerateConfig,
]
