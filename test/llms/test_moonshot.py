import unittest
from zlai.llms import MoonShot
from zlai.llms.generate_config.api.moonshot import *


class TestDouBao(unittest.TestCase):
    """"""
    def test_doubao(self):
        """"""
        models = [
            MoonShot8KV1GenerateConfig,
            MoonShot32KV1GenerateConfig,
            MoonShot128KV1GenerateConfig,
        ]

        for gen_config in models:
            llm = MoonShot(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
