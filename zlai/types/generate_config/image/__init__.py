from .base import *
from .kolors import *
from .flux import *
from typing import Union


TypeImageGenerateConfig = Union[
    TypeKolorsGenerate,
    TypeFLUXGenerate,
]
