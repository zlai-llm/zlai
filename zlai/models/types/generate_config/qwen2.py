from typing import Optional
from .base import InferenceGenerateConfig


__all__ = [
    "Qwen2InstructInferenceGenerateConfig",
    "Qwen215BInstructInferenceGenerateConfig",
    "Qwen205BInstructInferenceGenerateConfig",
]


class Qwen2InstructInferenceGenerateConfig(InferenceGenerateConfig):
    max_new_tokens: Optional[int] = 512
    top_k: Optional[int] = 20
    top_p: Optional[float] = 0.8
    do_sample: Optional[bool] = True
    temperature: Optional[float] = 0.7
    repetition_penalty: Optional[float] = 1.05


class Qwen205BInstructInferenceGenerateConfig(Qwen2InstructInferenceGenerateConfig):
    repetition_penalty: Optional[float] = 1.1


class Qwen215BInstructInferenceGenerateConfig(Qwen2InstructInferenceGenerateConfig):
    repetition_penalty: Optional[float] = 1.1

    