"""
Trading View
https://cn.tradingview.com/markets/world-stocks/worlds-largest-companies/

todo: 增加其他数据
todo: 增加Agent Tools测试
todo: 增加文档
"""

import requests
from typing import Dict, Literal, Optional, Annotated
from .base import *


__all__ = [
    "get_stock_technicals",
]


def get_stock_technicals(
        symbol: Annotated[Optional[str], "市场代码", True] = None,
        stock_code: Annotated[Optional[str], "股票代码", True] = None,
        time_period: Annotated[Literal["1min", "5min", "15min", "30min", "60min", "120min", "240min", "1day", "1week", "1month"], "时间周期", True] = "1day",
) -> Dict:
    """
    获取股票技术指标

    :param symbol:
    :param stock_code:
    :param time_period:
    :return:
    """
    url = trading_technicals_mapping.get(time_period)(symbol, stock_code)
    return requests.get(url, headers=headers).json()
