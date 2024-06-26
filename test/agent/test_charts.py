import unittest
import pandas as pd
from zlai.llms import Zhipu, GLM4AirGenerateConfig


class TestCharts(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.df = pd.read_csv("./test_data/titanic.csv")

    def test_data(self):
        """"""
        print(self.df.head().T)
        print(pd.DataFrame(self.df.groupby(by=["Pclass"])["Survived"].mean()).reset_index())
        print((self.df.groupby(by=["Siblings/Spouses Aboard"])["Survived"].mean()).to_markdown())

    def test_charts(self):
        """"""
        table = """
        |   Siblings/Spouses Aboard |   Survived |
        |--------------------------:|-----------:|
        |                         0 |   0.347682 |
        |                         1 |   0.535885 |
        |                         2 |   0.464286 |
        |                         3 |   0.25     |
        |                         4 |   0.166667 |
        |                         5 |   0        |
        |                         8 |   0        |"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig())
        chart = ChartAgent(llm=llm, verbose=True)

        query = "绘制一个图表，展示Siblings/Spouses Aboard和Survived的关系"

        task_completion = TaskCompletion(query=query, observation=table)
        out = chart(task_completion)
        print(out)
