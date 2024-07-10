import unittest
from typing import Literal
from zlai.tools.stock.sina import *


class TestSina(unittest.TestCase):

    def test_get_stock_rank_market(self):
        """"""
        markets = ["sh_a", "sh_b", "sz_a", "sz_b", "hk", "warn"]
        for market in markets:
            data = get_current_stock_rank(market=market, return_type="DataFrame")
            print(f"{market}: {data.shape}")

    def test_get_stock_rank_sort(self):
        """"""
        sorts = [
            "trade", "price_change", "change_percent", "buy", "sell", "settlement",
            "open", "high", "low", "volume", "amount",
        ]
        for sort in sorts:
            data = get_current_stock_rank(sort_by=sort, return_type="Markdown")
            print(f"{sort}")
            print(data)
            print()

