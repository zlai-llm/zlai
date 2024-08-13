import unittest
from openai import OpenAI


class TestEmbedding(unittest.TestCase):
    def test_embedding(self):
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.embeddings.create(input=["你好"], model="bge-m3")
        print(len(response.data[0].embedding))
        print(response.usage)
