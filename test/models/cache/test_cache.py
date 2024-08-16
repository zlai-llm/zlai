import unittest
import requests
from openai import OpenAI
from zlai.types import UserMessage


class TestModels(unittest.TestCase):
    def test_completion(self):
        """"""
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[
                UserMessage(content="Hello").model_dump(),
            ],
            stream=False
        )
        print(response)

        response = requests.post(url="http://localhost:8000/cache/current_models")
        print(response.json())

        # response = requests.post(url="http://localhost:8000/cache/drop_model", json={"method": ["load_qwen2"]})
        # print(response.json())

        response = requests.post(url="http://localhost:8000/cache/drop_model", json={"path": ['/home/models/Qwen/Qwen2-0.5B-Instruct']})
        print(response.json())

        response = requests.post(url="http://localhost:8000/cache/current_models")
        print(response.json())




