from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "TransferFundQueryConfig",
    "TransferFund",
]


class TransferFundQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "START_DATE", "END_DATE", "END_SETTLE_BALANCE", "AVG_SETTLE_BALANCE", "SETTLE_FUNDS_ADD",
            "SETTLE_FUNDS_REDUCE", "SETTLE_FUNDS_NET", "END_SETTLE_BALANCE_QOQ", "AVG_SETTLE_BALANCE_QOQ",
            "INDEX_PRICE_SH", "INDEX_PRICE_SZ", "INDEX_PRICE_CY", "INDEX_PRICE_ZX", "INDEX_CHANGE_RATIO_SH",
            "INDEX_CHANGE_RATIO_SZ", "INDEX_CHANGE_RATIO_CY", "INDEX_CHANGE_RATIO_ZX"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "END_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_BANKSECURITY_TRANSFER_FUND",
            "_": self._current_time(),
        }
        return params


class TransferFund(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[TransferFundQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = TransferFundQueryConfig.model_validate(kwargs)
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
            "description": "中国 交易结算资金(银证转账) 据投保基金公司2017年7月31日公告，该数据已停止更新。",
            "columns": {
                "START_DATE": "开始时间",
                "END_DATE": "截至时间",
                "END_SETTLE_BALANCE": "交易结算资金期末余额(亿)",
                "AVG_SETTLE_BALANCE": "交易结算资金日均余额(亿)",
                "SETTLE_FUNDS_ADD": "银证转账增加额(亿)",
                "SETTLE_FUNDS_REDUCE": "银证转账减少额(亿)",
                "SETTLE_FUNDS_NET": "银证转账变动净额(亿)",
                # "END_SETTLE_BALANCE_QOQ": "",
                # "AVG_SETTLE_BALANCE_QOQ": "",
                "INDEX_PRICE_SH": "上证指数收盘",
                "INDEX_PRICE_SZ": "深证指数收盘",
                # "INDEX_PRICE_CY": "",
                # "INDEX_PRICE_ZX": "",
                "INDEX_CHANGE_RATIO_SH": "上证指数涨跌幅",
                "INDEX_CHANGE_RATIO_SZ": "深证指数涨跌幅",
                # "INDEX_CHANGE_RATIO_CY": "",
                # "INDEX_CHANGE_RATIO_ZX": "",
            }
        })

