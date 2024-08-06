import unittest
from zlai.documents import *
from zlai.elasticsearch import *
from zlai.embedding import *


class TestLoadDocumentAndVector(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        model_path = "/home/models/BAAI/bge-m3"
        self.embedding = PretrainedEmbedding(model_path=model_path, batch_size=16, normalize_embeddings=True, max_len=4096)

    def test_load_document(self):
        """"""
        load_documents = LoadDocuments(embedding=self.embedding, verbose=True)
        vectored_documents = load_documents(path="../test_data/document")
        print(len(vectored_documents))
