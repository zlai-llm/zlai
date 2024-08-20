from .cosy_voice.generation import cosy_voice_generation


__all__ = [
    "tts_mapping"
]

tts_mapping = {
    **{"CosyVoice-300M-SFT": cosy_voice_generation},
}
