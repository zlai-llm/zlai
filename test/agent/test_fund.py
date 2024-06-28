import unittest
from zlai.llms import Zhipu, GLM4GenerateConfig, GLM4AirGenerateConfig
from zlai.tools import *
from zlai.agent import *


class TestFund(unittest.TestCase):
    """"""

    def setUp(self):
        """"""

    def test_get_current_fund(self):
        """"""
        data = get_current_fund(fund_code="008888")
        print(data)

    def test_get_fund_name(self):
        """"""
        data = search_fund(fund_code="008888")
        print(data)

        data = search_fund(fund_name="华夏军工安全")
        print(data)

    def test_basic_info(self):
        """"""
        data = get_fund_basic_info(fund_code="008888")
        print(data)

    def test_get_fund_company(self):
        """"""
        data = get_fund_company(company_name="长城基金")
        print(data)
        data = get_fund_company(company_code="80000155")
        print(data)

    def test_get_history(self):
        """"""
        data = get_fund_history(fund_code="008888", start_date="2024-05-30", end_date="2024-06-27")
        print(data)

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4GenerateConfig())
        tool_list = [
            search_fund, get_fund_basic_info, get_current_fund,
            get_current_fund, get_fund_company, get_fund_history
        ]
        tools = Tools(tool_list=tool_list)

        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("帮忙查询基金代码为008888的的名称、基金类型、基金拼音全称。")
        task_completion = agent("帮忙查询基金名称为东方新能源汽车混合的基金代码、基金类型、基金拼音简写")

        task_completion = agent("帮忙查询基金代码为008888的基金基本信息，并总结这只基金的基本信息。")
        task_completion = agent("帮忙查询基金代码为008888的当前行情。")
        task_completion = agent("帮忙查询基金公司为建信基金的公司代码")
        task_completion = agent("帮忙查询基金公司代码80404011的基金公司名称。")

        task_completion = agent("帮忙查询基金代码为008888在2024年5月10日至5月17日的历史行情，并做分析。")
        # print(task_completion.content)


