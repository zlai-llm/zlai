from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "CurrencySupplyQueryConfig",
    "CurrencySupply",
]


class CurrencySupplyQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASIC_CURRENCY", "BASIC_CURRENCY_SAME", "BASIC_CURRENCY_SEQUENTIAL",
            "CURRENCY", "CURRENCY_SAME", "CURRENCY_SEQUENTIAL", "FREE_CASH", "FREE_CASH_SAME",
            "FREE_CASH_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_CURRENCY_SUPPLY",
            "_": self._current_time(),
        }
        return params


class CurrencySupply(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[CurrencySupplyQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = CurrencySupplyQueryConfig.model_validate(kwargs)
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
            "description": "中国 货币供应量",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "BASIC_CURRENCY": "货币和准货币(M2)",
                "BASIC_CURRENCY_SAME": "M2-同比",
                "BASIC_CURRENCY_SEQUENTIAL": "M2-环比",
                "CURRENCY": "货币(M1)",
                "CURRENCY_SAME": "M1-同比",
                "CURRENCY_SEQUENTIAL": "M1-环比",
                "FREE_CASH": "流通中的现金(M0)",
                "FREE_CASH_SAME": "M0-同比",
                "FREE_CASH_SEQUENTIAL": "M0-环比",
            }
        })
