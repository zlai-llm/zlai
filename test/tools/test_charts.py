import unittest
import numpy as np
from zlai.tools.echarts import *
import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Pie, Radar, Scatter, Map


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
