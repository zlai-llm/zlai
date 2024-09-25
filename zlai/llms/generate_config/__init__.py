from .base import *
from .api import *
from .local import *

from typing import Union


TypeAPIGenerateConfig = Union[
    TypeAliGenerate, TypeAtomGenerate, TypeBaichuanGenerate, TypeBaiduGenerate,
    TypeDeepSeekGenerate, TypeDouBaoGenerate, TypeHunYuanGenerate, TypeMoonShotGenerate,
    TypeOpenAIGenerate, TypeSiliconFlowGenerate, TypeSparkGenerate, TypeStepFunGenerate,
    TypeYiGenerate, TypeZhipuGenerate,
]


TypeLocalGenerateConfig = Union[
    CodeGeexGenerateConfig,
    CodeGeex4All9BGenerateConfig,
    CodeGeex4All9BGGUFGenerateConfig,

    DeepSeekGenerateConfig,
    DeepSeekV2LiteChatGenerateConfig,
    DeepSeekCoderV2LiteInstructChatGenerateConfig,

    GLM4GenerateConfig,
    GLM4Chat9BGenerateConfig,
    GLM4Chat9B1MGenerateConfig,
    GLM4V9BGenerateConfig,
    GLM4LongWriter9B,
    Llama3LongWriter8B,

    MiniCPMV26GenerateConfig,

    Qwen2GenerateConfig,
    Qwen2Instruct05BGenerateConfig,
    Qwen2Instruct15BGenerateConfig,
    Qwen2Instruct7BGenerateConfig,
    Qwen2Audio7BInstructGenerateConfig,
    Qwen2VLInstructGenerateConfig,
    Qwen2VL7BInstructGenerateConfig,
    Qwen2VL2BInstructGenerateConfig,
]


TypeGenerateConfig = Union[
    GenerateConfig, BaseGenerateConfig, TypeAPIGenerateConfig, TypeLocalGenerateConfig
]
