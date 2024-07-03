import os
import unittest
from zlai.llms.step_fun import *
from zlai.llms.generate_config.step_fun import *


class TestMokeModels(unittest.TestCase):
    """"""
    def test_models(self):
        """"""
        llm = StepFun()
        print(llm._list_models())
        print(len(llm._list_models().data))

    def test_loop_config(self):
        """"""
        config = [
            Step8KV1GenerateConfig,
            Step32KV1GenerateConfig,
            Step1V8KGenerateConfig,
            Step1V32KGenerateConfig,
            Step128KV1GenerateConfig,
            Step256KV1GenerateConfig,
        ]
        for gen_config in config:
            llm = StepFun(generate_config=gen_config())
            data = llm.generate(query="你好")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
