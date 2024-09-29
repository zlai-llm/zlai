import unittest
from zlai.tools.report import *


class TestStockPerformance(unittest.TestCase):
    """"""
    def test_stock(self):
        """"""
        stock = StockPerformance(industry="酿酒行业", quarter="2024Q1", size=10)
        data = stock.load_data()
        print(data.metadata)
        print(data.to_frame(columns=data.metadata.get("columns")).to_markdown())

