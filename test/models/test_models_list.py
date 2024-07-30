import unittest
from openai import OpenAI
from zlai.llms import DeepSeek


class TestModels(unittest.TestCase):
    def test_models_list(self):
        """"""
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        print(client.models.list())

    def test_models_retrieve(self):
        client = DeepSeek()
        print(client._list_models())

