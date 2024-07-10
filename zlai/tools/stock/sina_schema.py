from pydantic import BaseModel, Field
from typing import Literal

__all__ = [
    "headers",
    # SINA
    "TypeSortBy",
    "TypeMarket",
    "sort_by_mapping",
    "market_mapping",
    # Schema
    "StockRankParams",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

# sina
TypeSortBy = Literal[
    "trade", "price_change", "change_percent", "buy", "sell", "settlement",
    "open", "high", "low", "volume", "amount",
]

sort_by_mapping = {
    "trade": "trade",                      # 最新价
    "price_change": "pricechange",         # 涨跌额
    "change_percent": "changepercent",     # 涨跌幅
    "buy": "buy",                          # 买入
    "sell": "sell",                        # 买出
    "settlement": "settlement",            # 昨日收盘
    "open": "open",                        # 今开
    "high": "high",                        # 最高
    "low": "low",                          # 最低
    "volume": "volume",                    # 成交量
    "amount": "amount",                    # 成交额
}

TypeMarket = Literal[
    "sh_a", "sh_b", "sz_a", "sz_b", "hk", "warn"
]

market_mapping = {
    "sh_a": "sh_a",        # 上海A
    "sh_b": "sh_b",        # 上海B
    "sz_a": "sz_a",        # 深圳A
    "sz_b": "sz_b",        # 深圳B
    "hk": "qbgg_hk",       # 香港
    "warn": "shfxjs",      # 风险警示
}


class StockRankParams(BaseModel):
    """"""
    page: int = Field(default=1, description="页码")
    num: int = Field(default=5, description="每页条数")
    sort: str = Field(default="change_percent", description="排序字段")
    asc: int = Field(default=0, description="升序")
    node: str = Field(default="sh_a", description="市场")
    symbol: str = Field(default="", description="板块")
