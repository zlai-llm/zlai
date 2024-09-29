from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "CPIQueryConfig",
    "CPI",
]


class CPIQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """"""
        columns = [
            "REPORT_DATE", "TIME", "NATIONAL_SAME", "NATIONAL_BASE", "NATIONAL_SEQUENTIAL",
            "NATIONAL_ACCUMULATE", "CITY_SAME", "CITY_BASE", "CITY_SEQUENTIAL", "CITY_ACCUMULATE",
            "RURAL_SAME", "RURAL_BASE", "RURAL_SEQUENTIAL", "RURAL_ACCUMULATE",
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_CPI",
            "_": self._current_time(),
        }
        return params


class CPI(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[CPIQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = CPIQueryConfig.model_validate(kwargs)
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
        中国 居民消费价格指数(CPI，上年同月=100)
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
            "description": "中国 居民消费价格指数(CPI，上年同月=100)",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "NATIONAL_SAME": "全国同期",
                "NATIONAL_BASE": "全国基期",
                "NATIONAL_SEQUENTIAL": "全国环比",
                "NATIONAL_ACCUMULATE": "全国累计",
                "CITY_SAME": "城市同期",
                "CITY_BASE": "城市基期",
                "CITY_SEQUENTIAL": "城市环比",
                "CITY_ACCUMULATE": "城市累计",
                "RURAL_SAME": "农村同期",
                "RURAL_BASE": "农村基期",
                "RURAL_SEQUENTIAL": "农村环比",
                "RURAL_ACCUMULATE": "农村累计",
            }
        })
