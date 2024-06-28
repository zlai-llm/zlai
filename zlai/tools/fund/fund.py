import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Union, Optional, Annotated
from pydantic import BaseModel, Field

from ...parse import ParseList, ParseDict
from .utils import *


__all__ = [
    "get_url",
    "CurrentFundData",
    "get_fund_basic_info",
    "get_current_fund",
    "search_fund",
    "get_fund_company",
    "get_fund_history",
]
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Referer': 'https://fundf10.eastmoney.com/',
}


def get_url(url):
    """"""
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    return res.text


def search_fund(
        fund_name: Annotated[Optional[str], '基金名称', True] = None,
        fund_code: Annotated[Optional[str], '基金代码', False] = None,
        max_: Annotated[Optional[int], '最大返回数量', False] = 10,
) -> Dict:
    """
    依据基金名称或者基金代码，获取基金代码、基金拼音简写、基金类型、基金拼音全称等信息

    :param fund_name: 基金名称
    :param fund_code: 基金代码
    :param max_: 最大返回数量
    :return:
    """
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    info = get_url(url)
    info = ParseList.greedy_list(info)[0]
    columns = ['基金代码', '基金拼音简写', '基金名称', '基金类型', '基金拼音全称']
    df = pd.DataFrame(info, columns=columns, dtype=str)
    if fund_code:
        data = df[df["基金代码"] == fund_code].to_dict("records")
        return data
    elif fund_name:
        data = df[df["基金名称"].str.contains(fund_name)].to_dict("records")[:max_]
        return data
    else:
        raise ValueError("fund_code or fund_name must be provided")


class CurrentFundData(BaseModel):
    """"""
    fundcode: str = Field(default="", description="基金代码")
    name: str = Field(default="", description="基金名称")
    jzrqv: str = Field(default="", description="上一交易日")
    dwjz: str = Field(default="", description="基金净值（截止上一交易日）")
    gsz: str = Field(default="", description="估算净值（实时）")
    gszzl: str = Field(default="", description="估算涨幅（实时）")
    gztime: str = Field(default="", description="更新时间（实时）")

    def mapping_data(self):
        """"""
        name = self.model_fields.keys()
        desc = [item.description for item in self.model_fields.values()]
        return name, desc

    def desc2name(self):
        """"""
        name, desc = self.mapping_data()
        return dict(tuple(zip(desc, name)))

    def name2desc(self):
        """"""
        name, desc = self.mapping_data()
        return dict(tuple(zip(name, desc)))

    def map_dict(self):
        """"""
        output = dict()
        mapping = self.name2desc()
        for k, v in self.model_dump().items():
            output[mapping[k]] = v
        return output


def get_fund_basic_info(
        fund_code: Annotated[str, '基金代码', True] = '000001',
) -> Dict:
    """
    依据基金代码获取基金的基本信息。基本信息包括:
        ['基金全称', '基金简称', '基金代码', '基金类型', '发行日期', '成立日期/规模', '资产规模', '份额规模', '基金管理人',
        '基金托管人', '基金经理人', '成立来分红', '管理费率', '托管费率',  '销售服务费率', '最高认购费率', '最高申购费率',
        '最高赎回费率', '业绩比较基准', '跟踪标的']

    :param fund_code: 基金代码
    :return: 基金基本信息
    """
    url = f"https://fundf10.eastmoney.com/jbgk_{fund_code}.html"
    text = get_url(url)
    soup = BeautifulSoup(text, 'lxml')
    table_info = soup.find_all('table', {'class': 'info w790'})[0]
    th = [item.text for item in table_info.find_all('th')]
    td = [item.text for item in table_info.find_all('td')]
    fund_basic_info = dict(zip(th, td))
    return fund_basic_info


def get_current_fund(
        fund_code: Annotated[str, '基金代码', True] = '000001',
) -> Union[Dict, str]:
    """
    依据基金代码，获取当前基金的净值、涨幅等信息。
    :param fund_code: 基金代码
    :return: 基金当前数据
    """
    url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
    text = get_url(url)
    data = ParseDict.eval_dict(text)
    if len(data) > 0:
        return CurrentFundData(**data[0]).map_dict()
    else:
        return f"未查询到 {fund_code} 的数据。"


def get_fund_company(
        company_name: Annotated[Optional[str], '基金公司名称', True] = None,
        company_code: Annotated[Optional[str], '基金公司代码', True] = None,
) -> List[Dict]:
    """
    给定基金公司代码查询基金公司名称，或给定基金公司名称查询基金公司代码

    :param company_name: 基金公司名称
    :param company_code: 基金公司代码
    :return:
    """
    url = "http://fund.eastmoney.com/js/jjjz_gs.js"
    info = get_url(url)
    data = ParseList.greedy_list(info)[0]
    columns = ['基金公司代码', '基金公司名称']
    df_data = pd.DataFrame(data, columns=columns)
    if company_code:
        data = df_data[df_data["基金公司代码"] == company_code].to_dict("records")
        return data
    elif company_name:
        data = df_data[df_data["基金公司名称"].str.contains(company_name)].to_dict("records")
        return data
    else:
        raise ValueError("fund_code or fund_name must be provided")


def get_fund_history(
        fund_code: Annotated[str, '基金代码', True],
        start_date: Annotated[str, '查询开始日期', True],
        end_date: Annotated[str, '查询结束日期', True],
) -> str:
    """
    给定基金代码、查询开始与结束日期，查询日期内该基金的历史行情信息。
    :param fund_code: 基金代码
    :param end_date: 查询开始日期, yyyy-MM-dd
    :param start_date: 查询结束日期, yyyy-MM-dd
    :return: 
    """
    columns = ['FSRQ', 'DWJZ', 'LJJZ', 'SDATE', 'ACTUALSYI', 'NAVTYPE', 'JZZZL', 'SGZT',
               'SHZT', 'FHFCZ', 'FHFCBZ', 'DTYPE', 'FHSP']
    col_mapping = {
        "FSRQ": "净值日期", "DWJZ": "单位净值", "LJJZ": "累计净值",
        "JZZZL": "日增长率", "SGZT": "申购状态", "SHZT": "赎回状态",
    }
    jq_callback = jquery_mock_callback()
    url = f"https://api.fund.eastmoney.com/f10/lsjz?callback={jq_callback}" \
          f"&fundCode={fund_code}&pageIndex={1}&pageSize={100}" \
          f"&startDate={start_date}&endDate={end_date}&_={get_current_timestamp()}"

    text = get_url(url)
    null, false = None, False
    fund_info = eval(text.replace(jq_callback, ''))
    df_fund = pd.DataFrame(fund_info.get('Data').get('LSJZList'))
    df_fund = df_fund[columns]
    df_fund = df_fund[list(col_mapping.keys())].rename(columns=col_mapping)
    data = df_fund.to_markdown(index=False)
    return data
