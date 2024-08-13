import unittest
from openai import OpenAI
# from openai.embeddings_utils import get_embedding, cosine_similarity


class TestEmbedding(unittest.TestCase):
    def test_embedding(self):
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        data = client.embeddings.create(input=["你好"], model="bge-m3").data[0].embedding
        print(data)
