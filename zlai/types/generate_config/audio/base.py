from pydantic import BaseModel


__all__ = [
    "VoiceGenerateConfig",
]


class VoiceGenerateConfig(BaseModel):
    """"""
    input: str
    voice: str

    def gen_kwargs(self):
        return {k: v for k, v in self.model_dump().items() if v is not None}
