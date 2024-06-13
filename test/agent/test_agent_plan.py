import unittest
from zlai.agent import *
from zlai.llms import Zhipu, GLM4GenerateConfig
from zlai.embedding import PretrainedEmbedding
from zlai.elasticsearch import get_es_con


class TestAgentPlan(unittest.TestCase):

    def setUp(self):
        """"""
        self.index_name = "news"
        self.hosts = "http://localhost:9200/"
        model_path = "/home/models/BAAI/bge-small-zh-v1.5/"
        con = get_es_con(hosts=self.hosts)
        self.embedding = PretrainedEmbedding(
            model_path=model_path,
            max_len=512,
            batch_size=16,
        )

        self.llm = Zhipu(generate_config=GLM4GenerateConfig())

        task_list = [
            TaskDescription(
                task=KnowledgeAgent, task_id=0, task_name="信息检索机器人",
                task_description="""可以从文本数据库中查询准确的信息，并以准确信息进行回答。""",
                task_parameters=TaskParameters(
                    verbose=True, use_memory=False, max_memory_messages=10,
                )
            ),
            TaskDescription(
                task=ChatAgent, task_id=1, task_name="聊天机器人",
                task_description="""提供普通对话聊天，不涉及专业知识与即时讯息。""",
                task_parameters=TaskParameters(
                    verbose=True, use_memory=False, max_memory_messages=10,
                )
            ),
            TaskDescription(
                task=Weather, task_id=2, task_name="天气播报机器人",
                task_description="""查询当前的天气数据，并为用户播报当前的天气信息""",
            ),
        ]

        self.knowledge = TaskPlan(
            task_list=task_list, llm=self.llm, embedding=self.embedding, verbose=True,
            max_memory_messages=10, index_name=self.index_name, elasticsearch_host=self.hosts
        )

    def test_agent_memory_chat(self):
        task_completion = self.knowledge("帮我查询杭州的天气，并从文本数据库中查询“旅游股2024年一季度合计净利润”。")
        print(len(self.knowledge.task_completions))
        print(task_completion.content)
