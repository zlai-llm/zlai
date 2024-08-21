from typing import Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "CodeGeexGenerateConfig",
    "CodeGeex4All9BGenerateConfig",
    "TypeCodeGeexGenerate",
]


class CodeGeexGenerateConfig(GenerateConfig):
    """"""
    do_sample: bool = True
    top_p: float = 0.8
    temperature: float = 0.8
    max_length: int = 8192
    num_beams: int = 1


class CodeGeex4All9BGenerateConfig(CodeGeexGenerateConfig):
    """"""


class CodeGeex4All9BGGUFGenerateConfig(CodeGeexGenerateConfig):
    """"""


TypeCodeGeexGenerate = Union[
    CodeGeexGenerateConfig,
    CodeGeex4All9BGenerateConfig,
    CodeGeex4All9BGGUFGenerateConfig,
]
