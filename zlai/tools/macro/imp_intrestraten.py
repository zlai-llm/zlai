from pydantic import Field
from typing import Any, Dict, Literal, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "ImpInterestQueryConfig",
    "ImpInterest",
]


class ImpInterestQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)
    market: Literal["上海", "中国", "伦敦", "欧洲", "香港", "新加坡"] = Field(default="上海")
    currency_code: Literal["CNY", "HKD", "USD", "GBP", "JPY", "EUR", "SGD"] = Field(default="CNY")
    indicator: Literal["1d", "1w", "2w", "1m", "3m", "6m", "9m", "1y"] = Field(default="1d")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _query_filter(self) -> str:
        """"""
        market_mapping = {"上海": "001", "中国": "002", "伦敦": "003", "欧洲": "004", "香港": "005", "新加坡": "006"}
        indicator_mapping = {
            "1d": "001",
            "1w": "101", "2w": "102",
            "1m": "201", "2m": "202", "3m": "203", "4m": "204", "5m": "205",
            "6m": "206", "7m": "207", "8m": "208", "9m": "209", "10m": "210", "11m": "211",
            "1y": "301",
        }
        _filter = f'(MARKET_CODE="{market_mapping.get(self.market)}")(CURRENCY_CODE="CNY")(INDICATOR_ID="{indicator_mapping.get(self.indicator)}")'
        return _filter

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "REPORT_PERIOD", "IR_RATE", "CHANGE_RATE", "INDICATOR_ID", "LATEST_RECORD",
            "MARKET", "MARKET_CODE", "CURRENCY", "CURRENCY_CODE",
        ]
        params = {
            "filter": self._query_filter(),
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_IMP_INTRESTRATEN",
            "_": self._current_time(),
        }
        return params


class ImpInterest(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[ImpInterestQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """
        :param size:
        :param currency_code: 币种
            ["CNY", "HKD", "USD", "GBP", "JPY", "EUR", "SGD"]
        :param market: 市场
            {"上海": "001", "中国": "002", "伦敦": "003", "欧洲": "004", "香港": "005", "新加坡": "006"}
        :param indicator: 指标周期
            {
                "1d": "001",
                "1w": "101", "2w": "102",
                "1m": "201", "2m": "202", "3m": "203", "4m": "204", "5m": "205",
                "6m": "206", "7m": "207", "8m": "208", "9m": "209", "10m": "210", "11m": "211",
                "1y": "301",
            }
        :param query_config:
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = ImpInterestQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """"""
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
        """"""
        metadata.update({
            "description": "CHIBOR即中国银行间同业拆借利率（China Interbank Offered Rate），1996年1月3日在中国人民银行总行的领导下，依托中国外汇交易中心的网络，12家商业银行总行和15家融资中心开始进行人民币联网拆借交易，全国性的同业拆借市场成立，并产生了CHIBOR。CHIBOR值以各银行同业拆借实际交易利率的加权平均值来确定。",
            "columns": {
                "REPORT_DATE": "时间",
                "REPORT_PERIOD": "周期",
                "IR_RATE": "利率(%)",
                "CHANGE_RATE": "涨跌(BP)",
                "INDICATOR_ID": "周期代码",
                "MARKET": "市场",
                "MARKET_CODE": "市场代码",
                "CURRENCY": "币种",
                "CURRENCY_CODE": "币种代码",
            }
        })
