import unittest
from zlai.agent import *
from zlai.llms import Zhipu, GLM4FlashGenerateConfig
from zlai.embedding import PretrainedEmbedding
from zlai.elasticsearch import get_es_con


class TestAgentMemory(unittest.TestCase):
    """"""

    def setUp(self):
        self.index_name = "news"
        self.hosts = "http://localhost:9200/"
        model_path = "/home/models/BAAI/bge-small-zh-v1.5/"
        con = get_es_con(hosts=self.hosts)
        self.embedding = PretrainedEmbedding(
            model_path=model_path,
            max_len=512,
            batch_size=16,
        )

        self.llm = Zhipu(generate_config=GLM4FlashGenerateConfig())

        self.knowledge = Knowledge(
            llm=self.llm, embedding=self.embedding, verbose=True,
            max_memory_messages=10, use_memory=True,
            index_name=self.index_name, elasticsearch_host=self.hosts)

    def test_agent_no_memory(self):
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
        ]

        knowledge = TaskSwitch(
            task_list=task_list, llm=self.llm, embedding=self.embedding, verbose=True,
            max_memory_messages=10, index_name=self.index_name, elasticsearch_host=self.hosts
        )

        task_completion = knowledge("你好")
        task_completion = knowledge(task_completion)
        print(len(self.knowledge.task_completions))
        print(task_completion.content)

    def test_agent_memory(self):
        task_completion = self.knowledge("你好吗？")
        print(len(self.knowledge.task_completions))
        task_completion = self.knowledge(task_completion)
        print(len(self.knowledge.task_completions))
        print(task_completion.content)

    def test_agent_memory_query(self):
        task_completion = self.knowledge("你好")
        task_completion = self.knowledge("你好")
        print(len(self.knowledge.task_completions))
        print(task_completion.content)

    def test_agent_memory_chat(self):
        task_completion = self.knowledge("闲聊模式，请记住：你的名字叫小刚，今年33岁，在读博士。")
        task_completion = self.knowledge("你好")
        task_completion = self.knowledge("旅游股2024年一季度合计净利润为？")
        task_completion = self.knowledge("你的名字是？")
        print(len(self.knowledge.task_completions))
        print(task_completion.content)


