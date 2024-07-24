import unittest


class TaskKnowledgeAgent(unittest.TestCase):
    def setUp(self):
        """"""
        self.host = ESUrl.url
        # self.llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.01))
        self.llm = LocalLLMAPI(generate_config=Qwen15Chat14BGenerateConfig(temperature=0.01))
        # model_path = "/home/models/BAAI/bge-m3"
        self.embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            # model_path=model_path,
            max_len=5000,
            max_len_error='split',
            batch_size=128,
            verbose=True,
        )

    def test_knowledge(self):
        """"""
        knowledge = KnowledgeAgent(
            llm=self.llm, embedding=self.embedding, verbose=True,
            index_name="data_assets", elasticsearch_host=self.host)
        answer = knowledge("什么是数据资产如表？")

    def test_knowledge_stream(self):
        """"""
        knowledge = KnowledgeAgent(
            llm=self.llm, embedding=self.embedding, verbose=True, stream=True,
            index_name="data_assets", elasticsearch_host=self.host)
        response = knowledge("什么是数据资产如表？", thresh=3)
        for resp in response:
            print(resp.content)

