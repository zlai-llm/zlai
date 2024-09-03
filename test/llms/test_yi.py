import unittest
from zlai.llms import Yi
from zlai.llms.generate_config.api.yi import *


class TestDouBao(unittest.TestCase):
    """"""
    def test_doubao(self):
        """"""
        models = [
            YiLargeGenerateConfig,
            YiMediumGenerateConfig,
            YiMedium200KGenerateConfig,
            YiSparkGenerateConfig,
            YiLargeRAGGenerateConfig,
            YiLargeTurboGenerateConfig,
            YiLargePreviewGenerateConfig,
            YiLargeRAGPreviewGenerateConfig,
        ]

        for gen_config in models:
            llm = Yi(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
