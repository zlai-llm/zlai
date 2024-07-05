"""
todo: 完成期货、股票、基金全部tools
todo: 增加期货、股票、基金全部Agent Tools
todo: 增加测试、文档
"""

import requests
import pandas as pd
from typing import List, Literal, Optional, Annotated
from .base import headers
from ..utils import *


__all__ = [
    "get_stock_kline_data",
    "get_futures_data",
]


def get_stock_kline_data(
        symbol: Annotated[str, "股票代码", True] = "sh000001",
        scale: Annotated[Optional[Literal[5, 15, 30, 60]], "时间间隔", False] = 5,
        data_len: Annotated[Optional[int], "数据长度", False] = 10,
        return_type: Annotated[Optional[Literal["DataFrame", "List", "Markdown"]], "返回类型", False] = "Markdown",
):
    """
    股票历史K-Line数据API

    :param symbol: 股票代码，如：sh000001
    :param scale: 时间间隔min，如：5，15，30，60
    :param data_len: 数据长度，如：10
    :param return_type: 返回类型，如：DataFrame, List
    :return: DataFrame
    """
    url = f"""https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={symbol}&scale={scale}&datalen={data_len}"""
    r = requests.get(url, headers=headers)
    data = r.json()
    data = pd.DataFrame(data)
    return trans_dataframe(data, return_type=return_type)


def get_futures_data(
        symbol: Annotated[str, "股票代码", True] = "AG2408",
        _type: Annotated[Optional[Literal["1min", "5min", "15min", "30min", "60min", "1day", "5day"]], "时间间隔", False] = "5min",
        return_type: Annotated[Optional[Literal["DataFrame", "List", "Markdown"]], "返回类型", False] = "Markdown",
):
    """
    商品期货历史数据API

    :param symbol: 期货代码，如：AG2408
    :param _type: 时间间隔，如：1min，5min，15min，30min，60min，1day，5day
    :param return_type: 返回类型，如：DataFrame, List
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
    return trans_dataframe(data, return_type=return_type)
