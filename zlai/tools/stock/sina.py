"""
todo: 完成期货、股票、基金全部tools
todo: 增加期货、股票、基金全部Agent Tools
todo: 增加测试、文档
"""

import requests
import pandas as pd
from typing import Literal, Optional, Annotated
from .sina_schema import *


__all__ = [
    "get_stock_kline_data",
    "get_futures_data",
    "get_current_stock_rank",
]


def get_stock_kline_data(
        symbol: Annotated[str, "股票代码", True] = "sh000001",
        scale: Annotated[Optional[Literal[5, 15, 30, 60]], "时间间隔", False] = 5,
        data_len: Annotated[Optional[int], "数据长度", False] = 10,
) -> pd.DataFrame:
    """
    股票历史K-Line数据API

    :param symbol: 股票代码，如：sh000001
    :param scale: 时间间隔min，如：5，15，30，60
    :param data_len: 数据长度，如：10
    :return: DataFrame
    """
    url = f"""https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={symbol}&scale={scale}&datalen={data_len}"""
    r = requests.get(url, headers=headers)
    data = r.json()
    data = pd.DataFrame(data)
    return data


def get_futures_data(
        symbol: Annotated[str, "股票代码", True] = "AG2408",
        _type: Annotated[Optional[Literal["1min", "5min", "15min", "30min", "60min", "1day", "5day"]], "时间间隔", False] = "5min",
) -> pd.DataFrame:
    """
    商品期货历史数据API

    :param symbol: 期货代码，如：AG2408
    :param _type: 时间间隔，如：1min，5min，15min，30min，60min，1day，5day
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


def get_current_stock_rank(
        market: Annotated[TypeMarket, "市场", False] = "sh_a",
        sort_by: Annotated[TypeSortBy, "排序字段", False] = "change_percent",
        num: Annotated[Optional[int], "返回条数", False] = 5,
        ascending: Annotated[Optional[Literal[0, 1]], "升序/降序", False] = 0,
) -> pd.DataFrame:
    """
    获取当前股票排名
    :param market: 市场
        如：sh_a: 上证A股; sh_b: 上证B股; sz_a: 深圳A股; sz_b: 深圳B股; hk: 港股, warn: 警示板
    :param sort_by: 排序字段
        如：最新价:trade, 涨跌额:price_change, 涨跌幅:change_percent, 买入:buy, 买出:sell,
        昨日收盘:settlement, 今开:open, 最高:high, 最低:low, 成交量:volume, 成交额:amount
    :param num: 返回数据条数
    :param ascending: 升序/降序，0：降序，1：升序
    :return: Union[DataFrame, List, Markdown]
    """
    if market == "hk":
        func_name = "getHKStockData"
    else:
        func_name = "getHQNodeData"
    base_url = f"https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.{func_name}"
    market = market_mapping.get(market)
    sort_by = sort_by_mapping.get(sort_by)
    params = StockRankParams(page=1, num=num, sort=sort_by, asc=ascending, node=market).model_dump()
    r = requests.get(base_url, params=params, headers=headers)
    data = r.json()
    data = pd.DataFrame(data)
    return data
