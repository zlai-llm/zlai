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


class TestCharts(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.tile = "test"
        self.sub_title = "sub_title"
        self.data = {"S-1": [1, 2, 3, 4, 5], "S-2": [1, 2.3, 3.9, 4.7, 5.2]}
        self.x_label = ["a", "b", "c", "d", "e"]

    def test_base_chart(self):
        """"""
        base_chart(x_ticks=self.x_label, data=self.data, title=self.tile, sub_title=self.sub_title)

    def test_map(self):
        """"""
        map_chart(
            data=[{"河北省": 1.2}, {"河南省": 1.3}, {"浙江省": 2.5}, {"广东省": 4.5}],
            title='2024年一季度GDP',
            sub_title='河北省、河南省、浙江省、广东省',
        )
