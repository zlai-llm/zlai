import unittest
from zlai.tools import *


class TestStock(unittest.TestCase):
    """"""
    def setUp(self):
        """"""

    def test_kline_data(self):
        """"""
        data = get_stock_kline_data()
        print(data)

    def test_get_future_data(self):
        """"""
        data = get_futures_data(symbol="AG2408", _type="1min")
        print(data.shape)
        print(data.head())

        data = get_futures_data(symbol="AG2408", _type="5min")
        print(data.shape)
        print(data.head())

        data = get_futures_data(symbol="AG2408", _type="1day")
        print(data.shape)
        print(data.head())

        data = get_futures_data(symbol="AG2408", _type="5day")
        print(data.shape)
        print(data.head())
