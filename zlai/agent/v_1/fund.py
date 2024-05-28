import re
import json
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from typing import *
import pandas as pd
from pydantic import Field
from ..utils import log
from ..parse import *
from .config import Config
from .agent import AgentOutput, register_tool, dispatch_tool, BaseAgent


__all__ = [
    "get_fund_tools",
    "fund_tools",
    "FundAgent",
]


config = Config()
FUND_TOOL_HOOKS = {}
FUND_TOOL_DESCRIPTIONS = []


class CurrentFundData(AgentOutput):
    """"""
    fundcode: str = Field(default="", description="基金代码")
    name: str = Field(default="", description="基金名称")
    jzrqv: str = Field(default="", description="上一交易日")
    dwjz: str = Field(default="", description="基金净值（截止上一交易日）")
    gsz: str = Field(default="", description="估算净值（实时）")
    gszzl: str = Field(default="", description="估算涨幅（实时）")
    gztime: str = Field(default="", description="更新时间（实时）")


def get_url(url):
    """"""
    res = requests.get(url, headers=config.headers)
    res.encoding = "utf-8"
    return res.text


@register_tool(tool_hooks=FUND_TOOL_HOOKS, tool_descriptions=FUND_TOOL_DESCRIPTIONS)
def get_all_fund(
        fund_name: Annotated[str, '基金名称', True] = '000001',
) -> Dict:
    """
    依据用户传入的基金名称，获取基金代码、基金拼音简写、基金类型、基金拼音全称等信息
    """
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    info = get_url(url)
    info = sparse_list(info)
    columns = ['基金代码', '基金拼音简写', '基金名称', '基金类型', '基金拼音全称']
    df = pd.DataFrame(info, columns=columns)
    data = df[df["基金名称"].str.contains(fund_name)].head(5).to_dict("records")
    return data


@register_tool(tool_hooks=FUND_TOOL_HOOKS, tool_descriptions=FUND_TOOL_DESCRIPTIONS)
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


@register_tool(tool_hooks=FUND_TOOL_HOOKS, tool_descriptions=FUND_TOOL_DESCRIPTIONS)
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


def get_fund_tools() -> List[dict]:
    return deepcopy(FUND_TOOL_DESCRIPTIONS)


def fund_tools(
        tool_name: str,
        tool_params: dict,
) -> str:
    """"""
    return dispatch_tool(tool_name=tool_name, tool_params=tool_params, hooks=FUND_TOOL_HOOKS)


class FundAgent(BaseAgent):
    tools: List[Dict] = get_fund_tools()
    dispatch_fun: Callable = fund_tools
    """"""
    def __init__(self, stream: Optional[bool] = False, verbose: bool = True):
        self.verbose = verbose
        self.stream = stream

    def dispatch_tool(self):
        """"""
        observation = fund_tools(
            tool_name=self.tool_name,
            tool_params=self.tool_params,
        )
        if self.verbose:
            log(text=f"""Observation: {observation}""")
        self.observation.content = observation
        self.observation.tool_call_id = self.tool_call_id
