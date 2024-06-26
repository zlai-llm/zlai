import unittest
from zlai.llms import Zhipu, GLM4AirGenerateConfig
from zlai.agent import Tools, ToolsAgent
from zlai.tools import *


class TestFund(unittest.TestCase):
    """"""

    def setUp(self):
        """"""

    def test_get_current_fund(self):
        """"""
        data = get_current_fund(fund_code="000001")
        print(data)

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        tools = Tools(function_list=[get_current_fund])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("帮忙查询基金代码为008888的当前行情数据。")
        print(task_completion.content)
