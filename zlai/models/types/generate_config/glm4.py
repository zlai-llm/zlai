from typing import Optional
from .base import InferenceGenerateConfig


__all__ = [
    "GLM49BInferenceGenerateConfig",
    "GLM49BChatInferenceGenerateConfig",
    "GLM49BChat1MInferenceGenerateConfig",
    "GLM4V9BInferenceGenerateConfig",
]


class GLM49BInferenceGenerateConfig(InferenceGenerateConfig):
    max_length: Optional[int] = 8192
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM49BChatInferenceGenerateConfig(InferenceGenerateConfig):
    max_length: Optional[int] = 128000
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM49BChat1MInferenceGenerateConfig(InferenceGenerateConfig):
    max_length: Optional[int] = 1024000
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8


class GLM4V9BInferenceGenerateConfig(InferenceGenerateConfig):
    max_length: Optional[int] = 8192
    top_p: Optional[float] = 0.8
    top_k: Optional[int] = 1
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.8

