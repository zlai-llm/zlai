from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeQwen2Generate",
    "Qwen2GenerateConfig",
    "Qwen2Instruct05BGenerateConfig",
    "Qwen2Instruct15BGenerateConfig",
    "Qwen2Instruct7BGenerateConfig",
    "Qwen2Audio7BInstructGenerateConfig",
    "Qwen2VLInstructGenerateConfig",
    "Qwen2VL7BInstructGenerateConfig",
    "Qwen2VL2BInstructGenerateConfig",
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


class Qwen2VLInstructGenerateConfig(GenerateConfig):
    """"""
    do_sample: Optional[bool] = True
    repetition_penalty: Optional[float] = 1.05
    temperature: Optional[float] = 0.1
    max_new_tokens: Optional[int] = 1024
    top_k: Optional[int] = 1
    top_p: Optional[float] = 0.001


class Qwen2VL7BInstructGenerateConfig(Qwen2VLInstructGenerateConfig):
    """"""


class Qwen2VL2BInstructGenerateConfig(Qwen2VLInstructGenerateConfig):
    """"""


TypeQwen2Generate = Union[
    Qwen2GenerateConfig,
    Qwen2Instruct05BGenerateConfig,
    Qwen2Instruct15BGenerateConfig,
    Qwen2Instruct7BGenerateConfig,
    Qwen2Audio7BInstructGenerateConfig,
    Qwen2VLInstructGenerateConfig,
    Qwen2VL7BInstructGenerateConfig,
    Qwen2VL2BInstructGenerateConfig,
]
