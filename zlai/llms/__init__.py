from .base import *
from .local import *
from .ali import *
from .zhipu import *
from .atom import *
from .moonshot import *
from .generate import *
from .generate_config import *

from typing import Union

TypeLLM = Union[Zhipu, LocalLLMAPI, Ali, Atom]
