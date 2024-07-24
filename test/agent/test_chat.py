import unittest
from zlai.llms import *
from zlai.agent import *


class TestChatAgent(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4AirGenerateConfig())

    def test_chat(self):
        """"""
        chat = ChatAgent(llm=self.llm)
        task_completion = chat(query="1+1=")
        print(task_completion.content)

    def test_chat_stream(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig(stream=True))
        chat = ChatAgent(llm=llm, stream=True, verbose=True)
        response = chat(query="你好")
        answer = ""
        for resp in response:
            answer += resp.delta
            print(answer)

    def test_local_chat_stream(self, ):
        """"""
        llm = LocalLLMAPI(generate_config=Qwen15Chat14BGenerateConfig(stream=True, incremental=True))
        chat = ChatAgent(llm=llm, stream=True, verbose=True)
        response = chat(query="介绍一下自己")
        answer = ""
        for resp in response:
            answer += resp.delta
            print(resp.delta)
