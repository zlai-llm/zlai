import unittest
import numpy as np
from zlai.elasticsearch import *
from zlai.types.documents import *
from zlai.types.elasticsearch import *


def get_doc():
    """"""
    data = {
        'page_content': 'https://example.com/1',
        'vector': np.random.rand(1024),
        'metadata': {"source": "https://example.com/1", "date": "2022-01-01", "title": "Example 1"}
    }
    return data


class TestCreateIndex(unittest.TestCase):

    def setUp(self):
        """"""
        self.hosts = "http://localhost:9200/"
        self.con = get_es_con(hosts=self.hosts)

    def test_create_index_exits(self):
        """"""
        create_index(index_name='test_index', field_schema=VectoredESDocument, reset=False, con=self.con, disp=True)

    def test_create_index_reset(self):
        """"""
        create_index(index_name='test_es_documents', field_schema=VectoredESDocument, reset=True, con=self.con, disp=True)

    def test_save_data(self):
        """"""
        data = [get_doc() for i in range(0, 20)]
        doc2es(data, index_name='test_es_documents', batch_size=2, con=self.con)


class TestSearch(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.hosts = "http://localhost:9200/"
        self.con = get_es_con(hosts=self.hosts)
        self.index_name = 'test_es_documents'

    def test_count(self):
        """"""
        self.tools = ElasticSearchTools(index_name=self.index_name, con=self.con)
        print(self.tools.count())

    def test_match_all(self):
        """"""
        self.tools = ElasticSearchTools(index_name=self.index_name, con=self.con)
        self.tools.match_context(match_type="match_all")
        data = self.tools.execute(3)
        print(len(data))

    def test_smi(self):
        """"""
        self.tools = ElasticSearchTools(index_name=self.index_name, con=self.con)
        vec = np.random.rand(1024).tolist()
        self.tools.cos_smi(vector=vec)
        data = self.tools.execute(3)
        print(len(data))
        for item in data:
            print(f'score: {item.get("_score")}')
            document = VectoredDocument.model_validate(item.get("_source"))
            print(document.page_content)
            print(len(document.vector))
            print(document.metadata, type(document.metadata))
