from .base import *
from .request import *
from .cosy_voice import *


from typing import Union


TypeAudioGenerateConfig = Union[
    VoiceGenerateConfig,
    CosyVoiceGenerateConfig,
]


audio_generate_config_mapping = {
    "CosyVoiceGenerateConfig": CosyVoiceGenerateConfig,
}
