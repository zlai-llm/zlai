from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "GDPQueryConfig",
    "GDP",
]


class GDPQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "DOMESTICL_PRODUCT_BASE", "FIRST_PRODUCT_BASE",
            "SECOND_PRODUCT_BASE", "THIRD_PRODUCT_BASE", "SUM_SAME", "FIRST_SAME",
            "SECOND_SAME", "THIRD_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_GDP",
            "_": self._current_time(),
        }
        return params


class GDP(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[GDPQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = GDPQueryConfig.model_validate(kwargs)
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
            "description": "中国 国内生产总值(GDP)",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "DOMESTICL_PRODUCT_BASE": "国内生产总值",
                "FIRST_PRODUCT_BASE": "第一产业绝对值（亿元）",
                "SECOND_PRODUCT_BASE": "第二产业绝对值（亿元）",
                "THIRD_PRODUCT_BASE": "第三产业绝对值（亿元）",
                "SUM_SAME": "国内生产总值同比增长",
                "FIRST_SAME": "第一产业同比增长",
                "SECOND_SAME": "第二产业同比增长",
                "THIRD_SAME": "第三产业同比增长",
            }
        })
