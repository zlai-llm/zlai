from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeGLM4Generate",
    "GLM4GenerateConfig",
    "GLM4Chat9BGenerateConfig",
    "GLM4Chat9B1MGenerateConfig",
    "GLM4V9BGenerateConfig",
    "GLM4LongWriter9B",
    "Llama3LongWriter8B",
]


class GLM4GenerateConfig(GenerateConfig):
    max_length: Optional[int] = 8192
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM4Chat9BGenerateConfig(GLM4GenerateConfig):
    max_length: Optional[int] = 128000
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM4Chat9B1MGenerateConfig(GLM4GenerateConfig):
    max_length: Optional[int] = 1024000
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM4V9BGenerateConfig(GLM4GenerateConfig):
    max_length: Optional[int] = 8192
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM4LongWriter9B(GenerateConfig):
    """"""
    max_length: int = 32768
    num_beams: int = 1
    do_sample: bool = True
    top_p: float = 0.8
    temperature: float = 0.8


class Llama3LongWriter8B(GenerateConfig):
    """"""
    max_new_tokens: int = 32768
    num_beams: int = 1
    do_sample: bool = True
    top_p: float = 0.8
    temperature: float = 0.5
    repetition_penalty: int = 1


TypeGLM4Generate = Union[
    GLM4GenerateConfig,
    GLM4Chat9BGenerateConfig,
    GLM4Chat9B1MGenerateConfig,
    GLM4V9BGenerateConfig,
    GLM4LongWriter9B,
    Llama3LongWriter8B,
]
