from typing import Literal
from .base import VoiceGenerateConfig


__all__ = [
    "CosyVoiceGenerateConfig"
]


class CosyVoiceGenerateConfig(VoiceGenerateConfig):
    """"""
    voice: Literal["中文女", "中文男", "日语男", "粤语女", "英文女", "英文男", "韩语女"] = "中文女"
