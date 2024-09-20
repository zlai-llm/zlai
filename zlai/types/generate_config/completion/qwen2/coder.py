from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig

__all__ = [
    "TypeQwen25CoderGenerate",
    "Qwen25CoderGenerateConfig",
    "Qwen25Coder15BInstructGenerateConfig",
    "Qwen25Coder7BInstructGenerateConfig",
]


class Qwen25CoderGenerateConfig(GenerateConfig):
    max_new_tokens: Optional[int] = 2048


class Qwen25Coder15BInstructGenerateConfig(Qwen25CoderGenerateConfig):
    """"""


class Qwen25Coder7BInstructGenerateConfig(Qwen25CoderGenerateConfig):
    """"""


TypeQwen25CoderGenerate = Union[
    Qwen25CoderGenerateConfig,
    Qwen25Coder15BInstructGenerateConfig,
    Qwen25Coder7BInstructGenerateConfig,
]
