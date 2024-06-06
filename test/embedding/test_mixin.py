import numpy as np
from typing import Any, List
from zlai.embedding import *
from zlai.schema import *
import unittest


class TestEmbeddingsResponded(unittest.TestCase):
    def setUp(self):
        self.vector1 = Vector(object="obj1", index=1, embedding=[0.1, 0.2, 0.3])
        self.vector2 = Vector(object="obj2", index=2, embedding=[0.4, 0.5, 0.6])
        self.embeddings_1 = EmbeddingsResponded(
            object="embedding",
            data=[self.vector1, self.vector2],
            model="model",
            usage=CompletionUsage(
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,)
            )

        self.vector3 = Vector(object="obj1", index=1, embedding=[0.1, 0.2, 0.3])
        self.vector4 = Vector(object="obj2", index=2, embedding=[0.9, 0.5, 0.6])
        self.embeddings_2 = EmbeddingsResponded(
            object="embedding",
            data=[self.vector3, self.vector4],
            model="model",
            usage=CompletionUsage(
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,)
        )

    def test_to_numpy(self):
        expected_result = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        result = self.embeddings_1.to_numpy()
        self.assertTrue(np.array_equal(result, expected_result))

        expected_result = np.array([[0.1, 0.2, 0.3], [0.9, 0.5, 0.6]])
        result = self.embeddings_2.to_numpy()
        self.assertTrue(np.array_equal(result, expected_result))


class TestEmbeddingMatch(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        model_path = "/home/models/BAAI/bge-small-zh-v1.5"

        self.embedding = Embedding(
            model_path=model_path,
            max_len=512,
            max_len_error='split',
            batch_size=2,
        )

    @classmethod
    def print_list(cls, data: List[Any]):
        """"""
        print(f"List: {len(data)}")
        for item in data:
            print(item)
        print()

    def test_emb(self):
        """"""
        data = embedding(url=EMBUrl.m3e_small, text=['你好', '你好'])
        print(len(data.data))

    def test_embedding(self):
        """"""
        vectors = self.embedding.embedding(text=tuple(['你好', '你好', '你好', '你好']))
        print(vectors.usage)
        print(len(vectors.data))

    def test_embedding_match_idx(self):
        """"""
        source = ['铁路']
        target = ['铁桥', '铁道', '火车', '雪糕']
        idx = self.embedding.match_idx(source=source, target=target, top_n=4)
        print(idx)

    def test_embedding_match(self):
        """"""
        source = ['铁路', '棒棒冰']
        target = ['铁桥', '铁道', '火车', '雪糕']
        idx = self.embedding.match(source=source, target=target, top_n=4)
        self.print_list(idx)

    def test_embedding_match_keywords(self):
        """"""
        source = ['铁路', '棒棒冰']
        target = ['铁路大桥', '铁桥', '铁道', '火车', '雪糕']
        data = self.embedding._match_keyword(source=source, target=target, thresh=0.6, keyword_method='keyword')
        self.print_list(data)

        data = self.embedding._match_keyword(source=source, target=target, thresh=0.7, keyword_method='content')
        self.print_list(data)

    def test_embedding_match_with_keywords(self):
        """"""
        # 功能测试
        source = ['铁路', '棒棒冰', '企业']
        target = ['铁路大桥', '铁桥', '铁道', '火车', '雪糕', '水蜜桃棒棒冰', "小微企业", '小型微利企业', '大型企业']
        data = self.embedding.match_with_keyword(
            source=source, target=target, thresh=(0.75, 0.6), keyword_method='keyword')
        self.print_list(data)

        data = self.embedding.match_with_keyword(
            source=source, target=target, thresh=(0.75, 0.6), keyword_method='keyword', drop_duplicate=False)
        self.print_list(data)

        data = self.embedding.match_with_keyword(
            source=source, target=target, thresh=(0.8, 0.7), keyword_method='content')
        self.print_list(data)

        # 异常测试
        with self.assertRaises(ValueError):
            source = ['铁路', '棒棒冰']
            target = []
            data = self.embedding.match_with_keyword(
                source=source, target=target, thresh=(0.75, 0.6), keyword_method='keyword')
            self.print_list(data)

            source = []
            target = ['铁路大桥', '铁桥', '铁道', '火车', '雪糕', '水蜜桃棒棒冰']
            data = self.embedding.match_with_keyword(
                source=source, target=target, thresh=(0.75, 0.6), keyword_method='keyword')
            self.print_list(data)
