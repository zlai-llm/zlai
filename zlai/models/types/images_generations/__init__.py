from .base import *
from .kolors import *
from .request import *
from .response import *

from typing import Union


TypeImageGenerateConfig = Union[
    ImageGenerateConfig,
    KolorsImageGenerateConfig,
]
