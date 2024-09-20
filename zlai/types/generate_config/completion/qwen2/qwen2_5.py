from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeQwen25Generate",
    "Qwen25GenerateConfig",
    "Qwen25Instruct05BGenerateConfig",
    "Qwen25Instruct15BGenerateConfig",
    "Qwen25Instruct3BGenerateConfig",
    "Qwen25Instruct7BGenerateConfig",
    "Qwen25Instruct14BGenerateConfig",
    "Qwen25Instruct32BGenerateConfig",
    "Qwen25Instruct72BGenerateConfig",
]


class Qwen25GenerateConfig(GenerateConfig):
    max_new_tokens: Optional[int] = 2048
    top_p: Optional[float] = 0.8
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.7
    repetition_penalty: Optional[float] = 1.05


class Qwen25Instruct05BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct15BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct3BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct7BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct14BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct32BGenerateConfig(Qwen25GenerateConfig):
    """"""


class Qwen25Instruct72BGenerateConfig(Qwen25GenerateConfig):
    """"""


TypeQwen25Generate = Union[
    Qwen25GenerateConfig,
    Qwen25Instruct05BGenerateConfig,
    Qwen25Instruct15BGenerateConfig,
    Qwen25Instruct3BGenerateConfig,
    Qwen25Instruct7BGenerateConfig,
    Qwen25Instruct14BGenerateConfig,
    Qwen25Instruct32BGenerateConfig,
    Qwen25Instruct72BGenerateConfig,
]
