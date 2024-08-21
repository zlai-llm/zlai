from typing import Optional, Union
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "TypeGLM4Generate",
    "GLM4GenerateConfig",
    "GLM4Chat9BGenerateConfig",
    "GLM4Chat9B1MGenerateConfig",
    "GLM4V9BGenerateConfig",
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


TypeGLM4Generate = Union[
    GLM4GenerateConfig,
    GLM4Chat9BGenerateConfig,
    GLM4Chat9B1MGenerateConfig,
    GLM4V9BGenerateConfig,
]
