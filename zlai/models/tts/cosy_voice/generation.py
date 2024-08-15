import io
import torchaudio
from typing import Union
from zlai.models.types.audio import *
from zlai.models.tts.cosy_voice.cosyvoice.cli.cosyvoice import CosyVoice


__all__ = [
    "cosy_voice_generation",
]


def cosy_voice_generation(
        cosy_voice: CosyVoice,
        generate_config: Union[VoiceGenerateConfig, CosyVoiceGenerateConfig],
) -> bytes:
    output = cosy_voice.inference_sft(tts_text=generate_config.input, spk_id=generate_config.voice)
    byte_io = io.BytesIO()
    torchaudio.save(byte_io, output["tts_speech"], 22050)
    wav_binary = byte_io.getvalue()
    return wav_binary
