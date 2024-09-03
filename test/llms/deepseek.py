import unittest
from zlai.llms.deepseek import *
from zlai.llms.generate_config.api.deepseek import *


class TestMokeModels(unittest.TestCase):
    """"""
    def test_models(self):
        """"""
        llm = DeepSeek()
        print(llm._list_models())

    def test_loop_config(self):
        """"""
        config = [
            DeepSeekChatGenerateConfig,
            DeepSeekCoderGenerateConfig,
        ]
        for gen_config in config:
            llm = DeepSeek(generate_config=gen_config())
            data = llm.generate(query="你好")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()


