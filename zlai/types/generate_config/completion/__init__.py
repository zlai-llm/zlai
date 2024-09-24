from .base import *
from .glm3 import *
from .glm4 import *
from .qwen1_5 import *
from .qwen2 import *
from .mini_cpm import *
from .deepseek import *
from .codegeex import *
from .stepfun import *
from typing import Union


TypeGenerateConfig = Union[
    GenerateConfig,
    TypeCodeGeexGenerate,
    TypeDeepSeekGenerate,
    TypeGLM3Generate,
    TypeGLM4Generate,
    TypeMiniCPMGenerate,
    TypeQwen15Generate,
    TypeQwen2Generate,
    TypeGotOCR2Generate,
]
