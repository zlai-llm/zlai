from typing import Literal, Union
from .base import VoiceGenerateConfig


__all__ = [
    "TypeCosyVoiceGenerate",
    "CosyVoiceGenerateConfig",
]


class CosyVoiceGenerateConfig(VoiceGenerateConfig):
    """"""
    voice: Literal["中文女", "中文男", "日语男", "粤语女", "英文女", "英文男", "韩语女"] = "中文女"


TypeCosyVoiceGenerate = Union[
    CosyVoiceGenerateConfig,
]
