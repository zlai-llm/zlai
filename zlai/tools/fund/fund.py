import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, Annotated
from pydantic import BaseModel, Field

from ...parse import ParseList


__all__ = [
    "CurrentFundData",
    "get_fund_basic_info",
    "get_current_fund_data",
    "get_all_fund",
]
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Referer': 'https://fundf10.eastmoney.com/',
}


class CurrentFundData(BaseModel):
    """"""
    fundcode: str = Field(default="", description="基金代码")
    name: str = Field(default="", description="基金名称")
    jzrqv: str = Field(default="", description="上一交易日")
    dwjz: str = Field(default="", description="基金净值（截止上一交易日）")
    gsz: str = Field(default="", description="估算净值（实时）")
    gszzl: str = Field(default="", description="估算涨幅（实时）")
    gztime: str = Field(default="", description="更新时间（实时）")


def get_fund_basic_info(
        fund_code: Annotated[str, '基金代码', True] = '000001',
) -> Dict:
    """
    依据用户传入的基金代码，获取基金的基本信息。
    """
    url = f"https://fundf10.eastmoney.com/jbgk_{fund_code}.html"
    text = get_url(url)
    soup = BeautifulSoup(text, 'lxml')
    table_info = soup.find_all('table', {'class': 'info w790'})[0]
    th = [item.text for item in table_info.find_all('th')]
    td = [item.text for item in table_info.find_all('td')]
    fund_basic_info = dict(zip(th, td))
    return fund_basic_info


def get_current_fund_data(
        fund_code: Annotated[str, '基金代码', True] = '000001',
) -> CurrentFundData:
    """
    依据用户传入的基金代码，获取当前基金的净值、涨幅等信息。
    """
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    text = get_url(url)
    fund_info = json.loads(re.findall(r'jsonpgz\((.*)\)', text)[0])
    return CurrentFundData(**fund_info).map_dict()


def get_all_fund(
        fund_name: Annotated[str, '基金名称', True] = '000001',
) -> Dict:
    """
    依据用户传入的基金名称，获取基金代码、基金拼音简写、基金类型、基金拼音全称等信息
    """
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    info = get_url(url)
    info = ParseList.eval_list(info)
    columns = ['基金代码', '基金拼音简写', '基金名称', '基金类型', '基金拼音全称']
    df = pd.DataFrame(info, columns=columns)
    data = df[df["基金名称"].str.contains(fund_name)].head(5).to_dict("records")
    return data


def get_url(url):
    """"""
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    return res.text
