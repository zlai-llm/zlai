import unittest
from zlai.llms.openai import *
from zlai.llms.generate_config.api.openai import *


class TestMokeModels(unittest.TestCase):
    """"""
    def test_models(self):
        """"""
        llm = OpenAI()
        print(llm._list_models())

    def test_loop_config(self):
        """"""
        config = [
            OpenAIGenerateConfig
        ]
        for gen_config in config:
            llm = OpenAI(generate_config=gen_config())
            data = llm.generate(query="你好")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
