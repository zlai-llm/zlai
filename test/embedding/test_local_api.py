import numpy as np
from zlai.embedding import *
from zlai.schema import *
import unittest


class TestEMB(unittest.TestCase):
    def setUp(self):
        """"""

    def test_bge_m3(self):
        """"""
        text = ['你好', '你好']
        embedding = OpenAIEmbedding(config=BGEM3EmbeddingConfig())
        data = embedding.embedding(text=tuple(text))
        print(data.to_numpy().shape)
