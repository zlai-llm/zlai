"""
todo: 完成期货、股票、基金全部tools
todo: 增加期货、股票、基金全部Agent Tools
todo: 增加测试、文档
"""

import requests
import pandas as pd
from typing import List, Literal, Optional, Annotated
from .base import headers


__all__ = [
    "get_stock_kline_data",
    "get_futures_data",
]


def get_stock_kline_data(
        symbol: Annotated[str, "股票代码", True] = "sh000001",
        scale: Annotated[Optional[Literal[5, 15, 30, 60]], "时间间隔", False] = 5,
        data_len: Annotated[Optional[int], "数据长度", False] = 10,
):
    """
    股票历史数据API
    :param symbol:
    :param scale:
    :param data_len:
    :return:
    """
    url = f"""https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={symbol}&scale={scale}&datalen={data_len}"""
    r = requests.get(url, headers=headers)
    data = r.json()
    data = pd.DataFrame(data)
    return data


# https://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesNewService.getMinLine?symbol=AG2408
# https://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesNewService.getFourDaysLine?symbol=AG2408
# https://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesNewService.getDailyKLine?symbol=AG2408
# https://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesNewService.getFewMinLine?symbol={symbol}&type={scale}
def get_futures_data(
        symbol: Annotated[str, "股票代码", True] = "AG2408",
        _type: Annotated[Optional[Literal["1min", "5min", "15min", "30min", "60min", "1day", "5day"]], "时间间隔", False] = "5min",
):
    """
    商品期货历史数据API:

    :return:
    """
    fun_mapping = {
        "getMinLine": ["1min"],
        "getFourDaysLine": ["5day"],
        "getDailyKLine": ["1day"],
        "getFewMinLine": ["5min", "15min", "30min", "60min"],
    }

    fun_name = None
    for fun_name, _types in fun_mapping.items():
        if _type in _types:
            break

    if fun_name is None:
        raise ValueError(f"{_type} is not supported")

    base_url = f"https://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesNewService.{fun_name}"
    if fun_name == "getFewMinLine":
        params = {"symbol": symbol, "type": _type}
    else:
        params = {"symbol": symbol}

    r = requests.get(base_url, params=params, headers=headers)
    data = r.json()
    if fun_name == "getFourDaysLine":
        days_data = [pd.DataFrame(day_data) for day_data in data]
        data = pd.concat(days_data, axis=0)
    else:
        data = pd.DataFrame(data)
    return data
