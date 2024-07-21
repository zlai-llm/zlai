from .ali import *
from .baichuan import *
from .base import *
from .zhipu import *
from .atom import *
from .moonshot import *
from .deepseek import *
from .doubao import *
from .hunyuan import *
from .openai import *
from .silicon_flow import *
from .spark import *
from .baidu import *
from .step_fun import *
from .yi import *
from .local import *

from typing import Union


TypeGenerateConfig = Union[
    GenerateConfig, BaseGenerateConfig, TypeLocalGenerate,
    TypeAliGenerate, TypeAtomGenerate, TypeBaichuanGenerate, TypeBaiduGenerate,
    TypeDeepSeekGenerate, TypeDouBaoGenerate, TypeHunYuanGenerate, TypeMoonShotGenerate,
    OpenAIGenerateConfig, TypeSiliconFlowGenerate, TypeSparkGenerate, TypeStepFunGenerate,
    TypeYiGenerate, TypeZhipuGenerate,
]
