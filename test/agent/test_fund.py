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


class TestFund(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4AirGenerateConfig(temperature=0.1))

    def test_fund_code(self):
        """"""
        fund = FundCodeAgent(llm=self.llm, verbose=True)
        query = "查询有关于000011的有关信息"
        query = "查询有关于009011的有关信息"
        query = "000011今天的行情怎么样？"
        query = "070011今天的行情怎么样？"
        out = fund(query)

    def test_fund_status(self):
        """"""
        fund = FundStatus(llm=self.llm, verbose=True)
        query = "000011今天的行情怎么样？"
        query = "A00011今天的行情怎么样"
        out = fund(query)

    def test_fund_information(self):
        """"""
        info = FundCode(llm=self.llm, verbose=True)
        # query = "查询有关于豆粕的基金代码"
        # query = "查询有关于有色金属的基金代码"
        # query = "查询有关于大成有色金属期货ETF联接A的基金代码"
        query = "查询有关于饮料的基金代码"
        out = info(query)

    def test_load_data(self):
        """"""
        import time
        import random

        class Constant:
            jQuery_Version = "1.8.3"

        def get_current_timestamp() -> int:
            return int(round(time.time() * 1000))

        def jquery_mock_callback() -> str:
            return f'jQuery{(Constant.jQuery_Version + str(random.random())).replace(".", "")}_{str(get_current_timestamp() - 1000)}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Referer': 'https://fundf10.eastmoney.com/',
        }

        url_dict = {
            'fund_basic': "http://fund.eastmoney.com/js/fundcode_search.js",  # 天天基金-所有基金基础数据
            'fund_company': 'http://fund.eastmoney.com/js/jjjz_gs.js'  # 天天基金-所有基金公司名称、代码
        }
        import requests
        def get_url(url):
            """"""
            res = requests.get(url, headers=headers)
            res.encoding = "utf-8"
            return res.text

        class GetFundHist():
            """
            FSRQ 净值日期
            DWJZ 单位净值
            LJJZ 累计净值
            SDATE
            ACTUALSYI
            NAVTYPE
            JZZZL 日增长率
            SGZT 申购状态
            SHZT 赎回状态
            FHFCZ
            FHFCBZ
            DTYPE
            FHSP    分红送配
            """

            def __init__(self):
                """"""
                self.columns = [
                    'FSRQ', 'DWJZ', 'LJJZ', 'SDATE', 'ACTUALSYI',
                    'NAVTYPE', 'JZZZL', 'SGZT', 'SHZT', 'FHFCZ',
                    'FHFCBZ', 'DTYPE', 'FHSP']

            def __call__(self, fund_code, start_date, end_date,
                         page_index=1, page_size=100, *args, **kwargs):
                """
                描述：获取基金历史净值

                参数：
                :param fund_code: 基金代码
                :param start_date: 开始时间
                :param end_date: 结束时间
                :param page_index: 页码数
                :param page_size: 单页数据条目数
                :param args:
                :param kwargs:
                :return:
                """
                self.fund_code = fund_code
                self.start_date = start_date
                self.end_date = end_date
                self.page_index = page_index
                self.page_size = page_size
                self.gen_url()
                self.sparse_info()

            def gen_url(self):
                self.jq_callback = jquery_mock_callback()
                self.url = f"https://api.fund.eastmoney.com/f10/lsjz?callback={self.jq_callback}" \
                           f"&fundCode={self.fund_code}&pageIndex={self.page_index}&pageSize={self.page_size}" \
                           f"&startDate={self.start_date}&endDate={self.end_date}&_={get_current_timestamp()}"

            def sparse_info(self):
                """"""
                text = get_url(self.url)
                null = None
                false = False
                self.fund_info = eval(text.replace(self.jq_callback, ''))
                self.total_count = self.fund_info.get('TotalCount')
                self.df_fund = pd.DataFrame(self.fund_info.get('Data').get('LSJZList'))
                self.df_fund = self.df_fund[self.columns]

        g = GetFundHist()
        g(fund_code="000001", start_date="2022-01-01", end_date="2022-01-31",)
        print(g.df_fund)
