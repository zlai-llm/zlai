import unittest
from zlai.types.messages.audio import AudioMessage


class TestMessage(unittest.TestCase):
    """"""

    def test_message(self):
        """"""
        from io import BytesIO
        from urllib.request import urlopen
        import librosa
        from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor
        path = "/home/models/Qwen/Qwen2-Audio-7B-Instruct"
        processor = AutoProcessor.from_pretrained(path)
        # model = Qwen2AudioForConditionalGeneration.from_pretrained(path, device_map="auto")

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
        # print(len(audios))
        # print([len(item) for item in audios])
