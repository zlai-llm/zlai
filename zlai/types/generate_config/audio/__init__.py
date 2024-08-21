from .base import *
from .cosy_voice import *
from typing import Union


TypeAudioGenerateConfig = Union[
    VoiceGenerateConfig,
    TypeCosyVoiceGenerate
]
