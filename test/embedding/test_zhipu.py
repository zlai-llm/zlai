from zlai.embedding import *
import unittest


class TestZhipuEmbedding(unittest.TestCase):
    def setUp(self):
        """"""

    def test_zhipu_embedding(self):
        """"""
        emb = ZhipuEmbedding(config=ZhipuEmbeddingConfig())
        response = emb.embedding(text=tuple(["你好", "你好"]))
        print(response.to_numpy().shape)
