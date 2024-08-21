from typing import Union, Literal
from pydantic import BaseModel


__all__ = [
    "SpeechRequest"
]


class SpeechRequest(BaseModel):
    """"""
    model: str
    """One of the available TTS models: tts-1 or tts-1-hd"""

    input: str
    """The text to generate audio for. The maximum length is 4096 characters."""

    voice: str
    """The voice to use when generating the audio. Supported voices are alloy, 
    echo, fable, onyx, nova, and shimmer. Previews of the voices are available in the Text to speech guide."""

    response_format: Union[str, Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]] = "wav"
    """The format to audio in. Supported formats are mp3, opus, aac, flac, wav, and pcm."""

    speed: Union[float] = 1.
    """The speed of the generated audio. Select a value from 0.25 to 4.0. 1.0 is the default."""

    def gen_kwargs(self):
        """"""
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return kwargs
