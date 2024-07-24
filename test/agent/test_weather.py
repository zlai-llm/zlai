import unittest
from zlai.llms import Zhipu, GLM4GenerateConfig, GLM40520GenerateConfig
from zlai.agent import Weather


class TestWeather(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4GenerateConfig())

    def test_weather(self):
        """"""
        weather = Weather(llm=self.llm, verbose=True)
        query = "杭州今天天气怎么样？"
        # query = "余杭今天天气怎么样？"
        # query = "余今天天气怎么样？"
        task_completion = weather(query=query)
        print(task_completion.content)
