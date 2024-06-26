import unittest
import numpy as np
from zlai.utils import *
from zlai.agent import *
from zlai.llms import *
from zlai.database import *
from zlai.elasticsearch import *
from zlai.embedding import *
from zlai.prompt import *
from zlai.retrievers import *
from zlai.schema import *
from zlai.parse import *
from zlai.streamlit import *
from typing import List
from zlai.utils import *


class TestImport(unittest.TestCase):

    def test_import(self):
        """"""
        print("Import Test.")


class TestLabelBySmi(unittest.TestCase):
    def test_empty_metrix(self):
        metrix = np.array([])
        labels = []
        expected_result = []
        result = label_by_smi(metrix, labels=labels)
        self.assertEqual(result, expected_result)

    def test_low_smis(self):
        metrix = np.array([[0.1, 0.2], [0.2, 0.3]])
        labels = ['A', 'B']
        expected_result = ['B']
        result = label_by_smi(metrix, labels=labels)
        self.assertEqual(result, expected_result)

    def test_high_smis(self):
        metrix = np.array([[0.8, 0.9], [0.7, 0.6]])
        labels = ['A', 'B']
        expected_result = ['A', 'B']
        result = label_by_smi(metrix, labels=labels)
        self.assertEqual(result, expected_result)

    def test_top(self):
        metrix = np.array([[0.4, 0.5], [0.4, 0.6]])
        labels = ['A', 'B']
        expected_result = ['B']
        result = label_by_smi(metrix, top=True, labels=labels)
        self.assertEqual(result, expected_result)

    def test_top_false(self):
        metrix = np.array([[0.8, 0.9], [0.7, 0.6]])
        labels = ['A', 'B']
        expected_result = ['A', 'B']
        result = label_by_smi(metrix, top=False, labels=labels)
        self.assertEqual(result, expected_result)

    def test_similarity_topn_idx(self):
        v_1 = np.random.random((1, 1024))
        v_2 = np.random.random((8, 1024))
        similarity = cosine_similarity(v_1, v_2.T)
        data = similarity_topn_idx(similarity, axis=1, top_n=len(v_2))
        print(data)


class TestChangeUrlPort(unittest.TestCase):
    def test_change_url_port(self):
        origin_port = 6501
        new_port = 3000
        urls = LLMUrl()
        urls.change_url_port(origin_port=origin_port, new_port=new_port)
        print(urls, type(urls))


class TestMessageAppend(unittest.TestCase):
    """"""
    def setUp(self):
        """"""

    def test_append_dict_to_json(self):
        """"""
        my_dict = {"name": "David", "age": 400, "city": "Los Angeles"}
        data = append_dict_to_json(my_dict, './data.json', 5)
        print(data)
