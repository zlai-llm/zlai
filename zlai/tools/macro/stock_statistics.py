from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "StockStatisticsQueryConfig",
    "StockStatistics",
]


class StockStatisticsQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=200)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "TOTAL_SHARES_SH", "TOTAL_MARKE_SH", "DEAL_AMOUNT_SH", "VOLUME_SH",
            "HIGH_INDEX_SH", "LOW_INDEX_SH", "TOTAL_SZARES_SZ", "TOTAL_MARKE_SZ", "DEAL_AMOUNT_SZ",
            "VOLUME_SZ", "HIGH_INDEX_SZ", "LOW_INDEX_SZ"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_STOCK_STATISTICS",
            "_": self._current_time(),
        }
        return params


class StockStatistics(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[StockStatisticsQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = StockStatisticsQueryConfig.model_validate(kwargs)
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
            "description": "中国 全国股票交易统计表",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "TOTAL_SHARES_SH": "发行总股本(SH)",
                "TOTAL_MARKE_SH": "市价总值(SH)",
                "DEAL_AMOUNT_SH": "成交金额(SH)",
                "VOLUME_SH": "成交量(SH)",
                "HIGH_INDEX_SH": "A股最高综合股价指数(SH)",
                "LOW_INDEX_SH": "A股最低综合股价指数(SH)",
                "TOTAL_SZARES_SZ": "发行总股本(SZ)",
                "TOTAL_MARKE_SZ": "市价总值(SZ)",
                "DEAL_AMOUNT_SZ": "成交金额(SZ)",
                "VOLUME_SZ": "成交量(SZ)",
                "HIGH_INDEX_SZ": "A股最高综合股价指数(SZ)",
                "LOW_INDEX_SZ": "A股最低综合股价指数(SZ)",
            }
        })
