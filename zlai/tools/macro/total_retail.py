from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "TotalRetailQueryConfig",
    "TotalRetail",
]


class TotalRetailQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "RETAIL_TOTAL", "RETAIL_TOTAL_SAME", "RETAIL_TOTAL_SEQUENTIAL",
            "RETAIL_TOTAL_ACCUMULATE", "RETAIL_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_TOTAL_RETAIL",
            "_": self._current_time(),
        }
        return params


class TotalRetail(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[TotalRetailQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = TotalRetailQueryConfig.model_validate(kwargs)
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
            "description": "中国 社会消费品零售总额 （每年2月公布当年1-2月累计值）",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "RETAIL_TOTAL": "当月(亿元)",
                "RETAIL_TOTAL_SAME": "同比增长",
                "RETAIL_TOTAL_SEQUENTIAL": "环比增长",
                "RETAIL_TOTAL_ACCUMULATE": "累计(亿元)",
                "RETAIL_ACCUMULATE_SAME": "累计同比增长",
            }
        })
