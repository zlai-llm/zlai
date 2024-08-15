from pydantic import BaseModel


__all__ = [
    "VoiceGenerateConfig",
]


class VoiceGenerateConfig(BaseModel):
    """"""
    input: str
    voice: str
