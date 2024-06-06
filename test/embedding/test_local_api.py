import numpy as np
from zlai.embedding import *
from zlai.schema import *
import unittest


class TestEMB(unittest.TestCase):
    def setUp(self):
        url = EMBUrl()
        url.change_url_port(origin_port=6501, new_port=3000)
        self.url = url

    def test_bge_large(self):
        vec = embedding(url=self.url.bge_large, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))

    def test_bge_base(self):
        vec = embedding(url=self.url.bge_base, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))

    def test_bge_small(self):
        vec = embedding(url=self.url.bge_small, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))
        print(vec[:10])

    def test_bge_m3(self):
        vec = embedding(url=self.url.bge_m3, text='你好', instruction=False, )
        print(len(vec), len(vec[0]))

    def test_m3e_large(self):
        vec = embedding(url=self.url.m3e_large, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))

    def test_m3e_base(self):
        vec = embedding(url=self.url.m3e_base, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))

    def test_m3e_small(self):
        vec = embedding(url=self.url.m3e_small, text='你好', instruction=False, )
        print(len(vec.to_numpy().shape))

    def test_m3e_lst(self):
        vec = embedding(
            url=self.url.m3e_large,
            text=['你好', '你好'],
            instruction=False,)
        print(np.array(vec).shape)

    def test_bge_lst(self):
        vec = embedding(
            url=self.url.bge_large,
            text=['你好', '你好'],
            instruction=False,)
        print(np.array(vec).shape)

    def test_embedding_timeout(self):
        """"""
        import requests
        with self.assertRaises(requests.exceptions.Timeout):
            embedding(url=self.url.bge_m3, text='你好', instruction=False, )
        # with self.assertRaises(requests.exceptions.RequestException):
        #     vec = embedding(url=self.url.bge_m3, text='你好', instruction=False, )

