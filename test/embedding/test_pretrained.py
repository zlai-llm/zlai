import unittest
from zlai.embedding import PretrainedEmbedding


class TestPretrainedEmbedding(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.model_path = "/home/models/BAAI/bge-small-zh-v1.5"

        self.embedding = PretrainedEmbedding(
            model_path=self.model_path,
            batch_size=2,
            normalize_embeddings=True,
            verbose=True,
        )

    def test_pretrained_embedding(self):
        """"""
        text = ["a", "b", "c", "c", "cs", "sda"]
        data = self.embedding.embedding(text=text)
        print(data.to_numpy().shape)


