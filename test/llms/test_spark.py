import unittest
from zlai.llms import Spark
from zlai.llms.generate_config.spark import *


class TestSpark(unittest.TestCase):

    def test_spark(self):
        """"""
        config = [
            SparkLiteGenerateConfig,
            SparkV2GenerateConfig,
            SparkProGenerateConfig,
            SparkMaxGenerateConfig,
            Spark4UltraGenerateConfig,
        ]
        for gen_config in config:
            llm = Spark(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(f"{gen_config.__name__.replace('GenerateConfig', '')}: {data.choices[0].message.content}")
            print()
