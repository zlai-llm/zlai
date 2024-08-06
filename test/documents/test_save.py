import unittest
from zlai.documents import *
from zlai.elasticsearch import *
from zlai.embedding import *
from zlai.types.elasticsearch import VectoredESDocument


class TestSaveDocumentToDB(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        model_path = "/home/models/BAAI/bge-m3"
        self.embedding = PretrainedEmbedding(model_path=model_path, batch_size=16, normalize_embeddings=True, max_len=4096)
        self.host = "http://localhost:9200/"
        self.index_name = "test_index"
        self.con = get_es_con(self.host)

    def test_save(self):
        """"""
        load_documents = LoadDocuments(embedding=self.embedding, verbose=True)
        vectored_documents = load_documents(path="../test_data/document")
        print(len(vectored_documents))

        save_documents = DocumentsToVectorDB(
            host=self.host, index_name=self.index_name, embedding=self.embedding,
            batch_size=16, thresh=1.95, verbose=True,
        )
        save_documents.reset_index(field_schema=VectoredESDocument)
        save_documents.save(data=vectored_documents)

        # validate
        self.tools = ElasticSearchTools(index_name=self.index_name, con=self.con)
        self.tools.match_context(match_type="match_all")
        data = self.tools.execute(10)
        print(len(data))
