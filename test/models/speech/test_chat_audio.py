from urllib.request import urlopen
from io import BytesIO
import base64
import unittest
from openai import OpenAI
from zlai.types.messages.audio import AudioMessage


class TestMessage(unittest.TestCase):
    """"""

    def test_bytes(self):
        """"""
        url = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/guess_age_gender.wav"
        data = urlopen(url).read()
        message = AudioMessage(content="", audios=[data])
        print(message)
        # print(message.to_message())

    def test_message(self):
        """"""
        conversation = [
            {"role": "user", "content": [
                {"type": "audio",
                 "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/guess_age_gender.wav"},
            ]},
            {"role": "assistant", "content": "Yes, the speaker is female and in her twenties."},
            {"role": "user", "content": [
                {"type": "audio",
                 "audio_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/translate_to_chinese.wav"},
            ]},
        ]

        message = AudioMessage(content="yes", audios_url=["https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/1272-128104-0000.flac"])

        print(message)
        print(message.get_audios(sr=16000))
        msg = message.to_message()
        other_msg = AudioMessage.model_validate(msg)
        other_msg.to_instance()
        print(other_msg)
        print(message.content[1].audio_url.getvalue() == other_msg.content[1].audio_url.getvalue())

    def test_audio_model(self):
        """"""
        message = AudioMessage(content="yes", audios_url=["https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/1272-128104-0000.flac"])

        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[message.to_message()],
            stream=False
        )
        print(response)
