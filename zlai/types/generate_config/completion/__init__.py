from .base import *
from .glm4 import *
from .qwen2 import *
from .mini_cpm import *
from .deepseek import *
from .codegeex import *
from typing import Union


TypeGenerateConfig = Union[
    GenerateConfig,
    TypeCodeGeexGenerate,
    TypeDeepSeekGenerate,
    TypeGLM4Generate,
    TypeMiniCPMGenerate,
    TypeQwen2Generate,
]
