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
        data = get_current_fund(fund_code="008888")
        print(data)

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        tools = Tools(function_list=[get_current_fund])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("帮忙查询基金代码为008888的当前行情数据。")
        print(task_completion.content)


import unittest
from zlai.agent import *
from zlai.embedding import *


class TestFundAgent(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            max_len=100,
            max_len_error='split',
            batch_size=128,
            verbose=True,
        )
        self.embedding = Embedding(
            model_path="/home/models/BAAI/bge-m3",
            max_len=100,
            max_len_error='split',
            batch_size=128,
            verbose=True,
        )

    def test_find_total_funds(self):
        """"""
        fund = FundAgent(verbose=True)
        data = fund.find_total_funds(fund_name="豆粕")
        print(data)

    def test_current_fund_data(self):
        """"""
        fund = FundAgent(verbose=True)
        # data = fund.find_current_fund_data(fund_code="007937")
        data = fund.find_current_fund_data(fund_code="007000")
        print(data)

    def test_fund_basic_info(self):
        """"""
        fund = FundAgent(verbose=True)
        # data = fund.find_current_fund_data(fund_code="007937")
        data = fund.find_fund_basic_info(fund_code="007000")
        print(data)

    def test_cache(self):
        """"""
        fund = FundAgent(verbose=True, embedding=self.embedding)
        fund.validate_cache()
