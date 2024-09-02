import os
from io import BytesIO
from typing import Annotated
from openai import OpenAI


__all__ = ["generate_audio"]


def generate_audio(
        prompt: Annotated[str, "需要转换为语音的文字", True],
) -> BytesIO:
    """
    生成音频的函数方法，给定文字返回音频。
    :param prompt:
    :return:
    """
    client = OpenAI(api_key="a", base_url=os.getenv("BASE_URL", "http://localhost:8000/"))
    audio_response = client.audio.speech.create(
        model="CosyVoice-300M-SFT", voice="中文女", input=prompt)
    audio = BytesIO(audio_response.content)
    return audio
