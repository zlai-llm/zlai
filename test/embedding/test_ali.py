from zlai.embedding import *
import unittest


class TestAliEmbedding(unittest.TestCase):
    def setUp(self):
        """"""
        self.config = AliEmbeddingV2Config()

    def test_ali_embedding(self):
        """"""
        emb = AliEmbedding(batch_size=1, config=AliEmbeddingV2Config())
        response = emb.embedding(
            text=tuple(["你好", "你好", "你好", "你好"])
        )
        print(response.to_numpy().shape)
        print(response.usage)
