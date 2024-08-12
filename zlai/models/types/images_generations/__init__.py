from .base import *
from .kolors import *
from .request import *
from .response import *

from typing import Union


TypeImageGenerateConfig = Union[
    ImageGenerateConfig,
    KolorsImageGenerateConfig,
    KolorsImage2ImageGenerateConfig,
]


images_generate_config_mapping = {
    "KolorsImageGenerateConfig": KolorsImageGenerateConfig,
    "KolorsImage2ImageGenerateConfig": KolorsImage2ImageGenerateConfig,
}
