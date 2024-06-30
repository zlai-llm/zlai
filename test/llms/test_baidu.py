import unittest
from zlai.llms import Baidu
from zlai.llms.generate_config.baidu import *


class TestBaidu(unittest.TestCase):
    """"""
    def test_baidu(self):
        """"""
        config = [
            ErnieSpeed8KGenerateConfig,
            ErnieSpeed128KGenerateConfig,
            ErnieSpeedAppBuilderGenerateConfig,
            ErnieLite8KGenerateConfig,
            ErnieLite8K0922GenerateConfig,
            ErnieTiny8KGenerateConfig,
        ]
        for gen_config in config:
            print(gen_config.__name__)
            llm = Baidu(generate_config=gen_config())
            completion = llm.generate(query="1+1=")
            print(completion.choices[0].message)

    def test_stream(self):
        """"""
        llm = Baidu(generate_config=ErnieSpeed8KGenerateConfig(stream=True))
        completions = llm.generate(query="你好。简单介绍下故宫。")
        for completion in completions:
            print(completion.choices[0].message.content)
