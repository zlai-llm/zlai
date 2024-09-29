from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "GoldCurrencyQueryConfig",
    "GoldCurrency",
]


class GoldCurrencyQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=200)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "GOLD_RESERVES", "GOLD_RESERVES_SAME", "GOLD_RESERVES_SEQUENTIAL",
            "FOREX", "FOREX_SAME", "FOREX_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_GOLD_CURRENCY",
            "_": self._current_time(),
        }
        return params


class GoldCurrency(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[GoldCurrencyQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = GoldCurrencyQueryConfig.model_validate(kwargs)
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
            "description": "中国 外汇和黄金储备",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "GOLD_RESERVES": "黄金储备(亿美元)",
                "GOLD_RESERVES_SAME": "黄金储备(同比)",
                "GOLD_RESERVES_SEQUENTIAL": "黄金储备(环比)",
                "FOREX": "国家外汇储备(亿美元)",
                "FOREX_SAME": "国家外汇储备(同比)",
                "FOREX_SEQUENTIAL": "国家外汇储备(环比)",
            }
        })
