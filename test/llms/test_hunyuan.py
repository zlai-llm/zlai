import unittest
from zlai.llms import HunYuan
from zlai.llms.generate_config.api.hunyuan import *


class TestHunYuan(unittest.TestCase):
    """"""
    def test_hunyuan(self):
        """"""
        config = [
            HunYuanLiteGenerateConfig,
            HunYuanStandardGenerateConfig,
            HunYuanStandard256KGenerateConfig,
            HunYuanProGenerateConfig,
        ]
        for gen_config in config:
            llm = HunYuan(generate_config=gen_config())
            completion = llm.generate(query="1+1=")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {completion.choices[0].message.content}")
            print()

    def test_stream(self):
        """"""
        llm = HunYuan(generate_config=HunYuanLiteGenerateConfig(stream=True))
        completions = llm.generate(query="1+1=")
        for completion in completions:
            print(completion.choices[0].message.content)
