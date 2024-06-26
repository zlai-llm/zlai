import unittest
from zlai.llms.baichuan import *
from zlai.llms.generate_config.baichuan import *


class TestMokeModels(unittest.TestCase):
    """"""
    def test_loop_config(self):
        """"""
        config = [
            Baichuan4GenerateConfig,
            Baichuan3TurboGenerateConfig,
            Baichuan3Turbo128kGenerateConfig,
            Baichuan2TurboGenerateConfig,
            Baichuan2Turbo192kGenerateConfig,
            BaichuanNPCTurboGenerateConfig,
            BaichuanNPCLiteGenerateConfig,
        ]
        for gen_config in config:
            llm = Baichuan(generate_config=gen_config())
            data = llm.generate(query="你好")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
