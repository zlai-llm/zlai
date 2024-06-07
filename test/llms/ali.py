import unittest
from zlai.llms.ali import *
from zlai.llms.generate_config.ali import *


class TestMokeAliModels(unittest.TestCase):
    """"""
    def test_loop_config(self):
        """"""
        config = [
            AliQwen2Instruct57BA14BGenerateConfig,
            AliQwen2Instruct72BGenerateConfig,
            AliQwenInstruct27BGenerateConfig,
            AliQwen2Instruct15BGenerateConfig,
            AliQwen2Instruct05BGenerateConfig,
        ]
        for gen_config in config:
            print(gen_config.__name__)
            llm = Ali(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(data.output.choices[0].message.content)
