from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "StockOpenQueryConfig",
    "StockOpen",
]


class StockOpenQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "STATISTICS_DATE", "ADD_INVESTOR", "ADD_INVESTOR_QOQ", "ADD_INVESTOR_YOY", "END_INVESTOR",
            "END_INVESTOR_A", "END_INVESTOR_B", "CLOSE_PRICE", "CHANGE_RATE", "TOTAL_MARKET_CAP",
            "AVERAGE_MARKET_CAP", "STATISTICS_DATE_NY",
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "STATISTICS_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_STOCK_OPEN_DATA",
            "_": self._current_time(),
        }
        return params


class StockOpen(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[StockOpenQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = StockOpenQueryConfig.model_validate(kwargs)
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
            "description": "中国 股票账户统计详细数据",
            "columns": {
                "STATISTICS_DATE": "数据日期",
                "ADD_INVESTOR": "新增投资者(万户)",
                "ADD_INVESTOR_QOQ": "新增投资者(环比)",
                "ADD_INVESTOR_YOY": "新增投资者(同比)",
                "END_INVESTOR": "期末投资者(万户)",
                "END_INVESTOR_A": "期末投资者(A股)",
                "END_INVESTOR_B": "期末投资者(B股)",
                "CLOSE_PRICE": "上证指数(收盘)",
                "CHANGE_RATE": "上证指数(涨跌幅)",
                "TOTAL_MARKET_CAP": "沪深总市值",
                "AVERAGE_MARKET_CAP": "沪深户均市值",
                "STATISTICS_DATE_NY": "月份"
            }
        })
