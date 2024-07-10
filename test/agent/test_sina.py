import unittest
from zlai.llms import Zhipu, GLM4AirGenerateConfig
from zlai.tools.stock.sina import *
from zlai.agent import *


class TestSina(unittest.TestCase):

    def test_get_stock_rank_market(self):
        """"""
        markets = ["sh_a", "sh_b", "sz_a", "sz_b", "hk", "warn"]
        for market in markets:
            data = get_current_stock_rank(market=market)
            print(f"{market}: {data.shape}")

    def test_get_stock_rank_sort(self):
        """"""
        sorts = [
            "trade", "price_change", "change_percent", "buy", "sell", "settlement",
            "open", "high", "low", "volume", "amount",
        ]
        for sort in sorts:
            data = get_current_stock_rank(sort_by=sort)
            print(f"{sort}")
            print(data)
            print()

    def test_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4AirGenerateConfig())
        tool_list = [get_current_stock_rank]
        tools = Tools(tool_list=tool_list)

        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("帮我分析一下上证股市的涨幅最大的10只股票。")

        print(task_completion.content)
