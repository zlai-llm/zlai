import unittest
from pathlib import Path
from openai import OpenAI
client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")


class TestSpeech(unittest.TestCase):
    """"""

    def test_file(self):
        import zlai.models.tts.cosy_voice

    def test_speech(self):
        """"""
        speech_file_path = Path(__file__).parent / "speech.wav"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Today is a wonderful day to build something people love!"
        )
        response.stream_to_file(speech_file_path)

