import unittest
from zlai.embedding import PretrainedEmbedding


class TestPretrainedEmbedding(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.model_path = "/home/models/BAAI/bge-small-zh-v1.5"

    def test_pretrained_embedding(self):
        """"""
        model_path = "/home/models/BAAI/bge-small-zh-v1.5"
        embedding = PretrainedEmbedding(
            model_path=model_path,                  # 模型路径
            batch_size=2,                           # 数据计算每批次样本数量
            normalize_embeddings=True,              # 是否归一化词向量
            verbose=True,                           # 是否打印日志
        )
        text = ["你好", "你是谁", "你这里有点好看", "如何打车去南京路", "我想吃西瓜", "今天去做点什么呢"]
        data = embedding.embedding(text=text)
        print(data.to_numpy().shape)

    def test_top_n_idx(self):
        """"""
        from zlai.embedding import Embedding

        model_path = "/home/models/BAAI/bge-small-zh-v1.5"
        embedding = Embedding(
            model_path=model_path,
            batch_size=16,
            normalize_embeddings=True,
            verbose=True,
        )
        target = [
            "谁更容易避免损失，谁的责任更大，谁更需要主动采取措施防止问题发声",
            "在这个事件中，女子的行为绝对责任占大头",
            "首先，网约车迟到并不是小概率事件，偶尔发生是可预判的",
            "而且网约车是无法知道乘客去机场剩余多少时间值机，也不知道你坐飞机去做什么",
            "换句话说，网约车的责任和平时迟到八分钟没有区别",
        ]

        query = "谁的责任占大头？"
        top_n_idx = embedding.match_idx(
            source=[query],
            target=target,
            top_n=2,
            filter='top_n',
        )
        print(top_n_idx)
        for idx in top_n_idx[0]:
            print(f"{idx} - {target[idx]}")

        query = ["谁的责任占大头？", "网约车是否知道乘客去机场剩余多少时间值机？"]
        top_n_idx = embedding.match_idx(
            source=query,
            target=target,
            top_n=2,
            filter='top_n',
        )
        print(top_n_idx)




