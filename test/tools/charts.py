import unittest
from zlai.tools import transform_tool_params
from zlai.tools.echarts import map_chart
from zlai.agent import Tools
from bs4 import BeautifulSoup
import inspect


class TestMapChart(unittest.TestCase):
    """"""
    def test_map_chart(self):
        """"""
        data = {
            "data": {
                "Items": [
                    {
                        "河北省": 5.2
                    },
                    {
                        "河南省": 7.3
                    },
                    {
                        "浙江省": 2.5
                    },
                    {
                        "广东省": 3.5
                    }
                ]
            },
            "data_source": "农业部",
            "sub_title": "河北省、河南省、浙江省、广东省",
            "title": "2024年一季度粮食收获"
        }
        data = transform_tool_params(data)
        print(data)
        tools = Tools(tool_list=[map_chart])
        answer = tools.dispatch_tool(tool_name="map_chart", tool_params=data)
        print(answer)
