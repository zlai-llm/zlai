import time
from pydantic import Field
from typing import Any, Dict, Union, Literal, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "StockPerformanceQueryConfig",
    "StockPerformance",
]


TypeSortBy = Literal[
    "BASIC_EPS", "BPS", "TOTAL_OPERATE_INCOME", "WEIGHTAVG_ROE", "PARENT_NETPROFIT",
    "MGJYXJJE",
]


class StockPerformanceQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=5)
    report_date: Optional[str] = Field(default=None)
    code: Optional[Union[str, int]] = Field(default=None)
    quarter: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)
    sort_by: Optional[TypeSortBy] = Field(default="BPS")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _query_filter(self) -> str:
        """"""
        condition = []
        if self.report_date:
            condition.append(f'(REPORTDATE="{self.report_date}")')
        if self.code:
            condition.append(f'(SECURITY_CODE="{self.code}")')
        if self.quarter:
            condition.append(f'(QDATE="{self.quarter}")')
        if self.industry:
            condition.append(f'(PUBLISHNAME="{self.industry}")')
        _filter = ''.join(condition)
        return _filter

    def to_params(self) -> Dict:
        """
        :return:
        """
        params = {
            "sortColumns": self.sort_by,
            "sortTypes": -1,
            "pageSize": self.size,
            "pageNumber": 1,
            "reportName": "RPT_LICO_FN_CPD",
            "columns": "ALL",
            "filter": self._query_filter(),
            "page_size": self.size,
            "_": str(int(time.time() * 1E3)),
        }
        return params


class StockPerformance(BaseRequestData):
    """新闻数据"""
    def __init__(
            self,
            query_config: Optional[StockPerformanceQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param size:
        :param query_config:
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = StockPerformanceQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """股票业绩"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        return base_url

    def load_data(self) -> ResponseData:
        """
        :return:
        """
        metadata = self.request_json().get("result", {})
        data = metadata.pop("data")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """股票业绩"""
        metadata.update({
            "description": "股票业绩",
            "columns": {
                "SECURITY_CODE": "证券代码",
                "SECURITY_NAME_ABBR": "证券简称",
                "TRADE_MARKET_CODE": "交易市场代码",
                "TRADE_MARKET": "交易市场",
                "SECURITY_TYPE_CODE": "证券类型代码",
                "SECURITY_TYPE": "证券类型",
                "UPDATE_DATE": "更新日期",
                "REPORTDATE": "报告日期",
                "BASIC_EPS": "基本每股收益",
                "DEDUCT_BASIC_EPS": "扣除后的基本每股收益",
                "TOTAL_OPERATE_INCOME": "总营业收入",
                "PARENT_NETPROFIT": "母公司净利润",
                "WEIGHTAVG_ROE": "加权平均净资产收益率",
                "YSTZ": "预计投资",
                "SJLTZ": "实际投资",
                "BPS": "每股净资产",
                "MGJYXJJE": "每股经营现金流量",
                "XSMLL": "销售毛利率",
                "YSHZ": "预计收益回报",
                "SJLHZ": "实际利润回报",
                "ASSIGNDSCRPT": "分配描述",
                "PAYYEAR": "分配年度",
                "PUBLISHNAME": "发布名称",
                "ZXGXL": "最新公告",
                "NOTICE_DATE": "公告日期",
                "ORG_CODE": "机构代码",
                "TRADE_MARKET_ZJG": "交易市场指标",
                "ISNEW": "是否新数据",
                "QDATE": "报告季度",
                "DATATYPE": "数据类型",
                "DATAYEAR": "数据年度",
                "DATEMMDD": "数据月份日期",
                "EITIME": "导出时间",
                "SECUCODE": "证券代号"
            }
        })
