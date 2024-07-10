from .base import *
from .ali import *
from .atom import *
from .baichuan import *
from .baidu import *
from .deepseek import *
from .doubao import *
from .hunyuan import *
from .moonshot import *
from .silicon_flow import *
from .spark import *
from .step_fun import *
from .yi import *
from .zhipu import *

from .local import *
from .generate import *
from .generate_config import *

from typing import Union

TypeLLM = Union[
    Ali, Atom, Baichuan, Baidu, DeepSeek, DouBao, HunYuan,
    MoonShot, SiliconFlow, Spark, StepFun, Yi, Zhipu,
    LocalLLMAPI, OpenAICompletion,
]

# todo 增加天工API https://model-platform.tiangong.cn/api-reference
# todo MiniMax https://www.minimaxi.com/
# todo ChatGPT https://api.openai.com/
# todo Azure OpenAI Service https://azure.microsoft.com/en-us/products/ai-services/openai-service
# todo Gimini https://makersuite.google.com/app/apikey
# todo 增加商汤大模型
# todo 增加Link-ai https://docs.link-ai.tech/platform/api/chat

