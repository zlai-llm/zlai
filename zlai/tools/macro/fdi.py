from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "FDIQueryConfig",
    "FDI",
]


class FDIQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "ACTUAL_FOREIGN", "ACTUAL_FOREIGN_SAME",
            "ACTUAL_FOREIGN_SEQUENTIAL", "ACTUAL_FOREIGN_ACCUMULATE", "FOREIGN_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_FDI",
            "_": self._current_time(),
        }
        return params


class FDI(BaseRequestData):
    """中国 外商直接投资数据(FDI)"""
    def __init__(
            self,
            query_config: Optional[FDIQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = FDIQueryConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def _base_url(self) -> str:
        """中国 外商直接投资数据(FDI)"""
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
        """中国 外商直接投资数据(FDI)"""
        metadata.update({
            "description": "中国 外商直接投资数据(FDI)",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "ACTUAL_FOREIGN": "当月(亿美元)",
                "ACTUAL_FOREIGN_SAME": "同比增长",
                "ACTUAL_FOREIGN_SEQUENTIAL": "环比增长",
                "ACTUAL_FOREIGN_ACCUMULATE": "累计(亿美元)",
                "FOREIGN_ACCUMULATE_SAME": "同比增长",
            }
        })
