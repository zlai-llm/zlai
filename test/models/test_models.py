import unittest
from openai import OpenAI


class TestModels(unittest.TestCase):
    def test_completion(self):
        """"""
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        print(response)

    def test_completion_stream(self):
        """"""
        client = OpenAI(
            api_key="fake-api-key",
            base_url="http://localhost:8000"
        )

        stream = client.chat.completions.create(
            model="mock-gpt-model",
            messages=[{"role": "user", "content": "Say this is a test"}],
            stream=True,
        )
        for chunk in stream:
            print(chunk)
