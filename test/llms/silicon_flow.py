import unittest
from zlai.llms.silicon_flow import *
from zlai.llms.generate_config.silicon_flow import *


class TestMokeModels(unittest.TestCase):
    """"""
    def test_loop_config(self):
        """"""
        config = [
            Qwen2Instruct7BGenerateConfig,
            Qwen2Instruct15BGenerateConfig,
            Qwen15Chat7BGenerateConfig,
            GLM3Chat6BGenerateConfig,
            GLM4Chat9BGenerateConfig,
            Yi15Chat6BGenerateConfig,
            Yi15Chat9BGenerateConfig,
        ]
        for gen_config in config:
            llm = SiliconFlow(generate_config=gen_config())
            data = llm.generate(query="你好")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
