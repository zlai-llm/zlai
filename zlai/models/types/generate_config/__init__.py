from .base import *
from .glm4 import *
from .qwen2 import *
from typing import Union


TypeInferenceGenerateConfig = Union[
    InferenceGenerateConfig,
    GLM49BInferenceGenerateConfig,
    GLM49BChatInferenceGenerateConfig,
    GLM49BChat1MInferenceGenerateConfig,
    GLM4V9BInferenceGenerateConfig,
    Qwen2InstructInferenceGenerateConfig,
    Qwen215BInstructInferenceGenerateConfig,
    Qwen205BInstructInferenceGenerateConfig,
]

inference_generate_config_mapping = {
    "GLM49BInferenceGenerateConfig": GLM49BInferenceGenerateConfig,
    "GLM49BChatInferenceGenerateConfig": GLM49BChatInferenceGenerateConfig,
    "GLM49BChat1MInferenceGenerateConfig": GLM49BChat1MInferenceGenerateConfig,
    "GLM4V9BInferenceGenerateConfig": GLM4V9BInferenceGenerateConfig,
    "Qwen2InstructInferenceGenerateConfig": Qwen2InstructInferenceGenerateConfig,
    "Qwen215BInstructInferenceGenerateConfig": Qwen215BInstructInferenceGenerateConfig,
    "Qwen205BInstructInferenceGenerateConfig": Qwen205BInstructInferenceGenerateConfig,
}

