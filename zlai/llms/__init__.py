from .base import *
from .ali import *
from .atom import *
from .baichuan import *
from .baidu import *
from .deepseek import *
from .doubao import *
from .moonshot import *
from .silicon_flow import *
from .spark import *
from .yi import *
from .zhipu import *

from .local import *
from .generate import *
from .generate_config import *

from typing import Union

TypeLLM = Union[
    Ali, Atom, Baichuan, Baidu, DeepSeek, DouBao,
    MoonShot, SiliconFlow, Spark, Yi, Zhipu, LocalLLMAPI,
]
