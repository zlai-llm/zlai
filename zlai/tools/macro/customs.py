from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "CustomsQueryConfig",
    "Customs",
]


class CustomsQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "EXIT_BASE", "IMPORT_BASE", "EXIT_BASE_SAME", "IMPORT_BASE_SAME",
            "EXIT_BASE_SEQUENTIAL", "IMPORT_BASE_SEQUENTIAL", "EXIT_ACCUMULATE", "IMPORT_ACCUMULATE",
            "EXIT_ACCUMULATE_SAME", "IMPORT_ACCUMULATE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_CUSTOMS",
            "_": self._current_time(),
        }
        return params


class Customs(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[CustomsQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = CustomsQueryConfig.model_validate(kwargs)
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
            "description": "中国 海关进出口增减情况一览表",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "EXIT_BASE": "当月出口额（亿美金）",
                "IMPORT_BASE": "当月进口额（亿美金）",
                "EXIT_BASE_SAME": "当月出口额（同比）",
                "IMPORT_BASE_SAME": "当月进口额（同比）",
                "EXIT_BASE_SEQUENTIAL": "当月出口额（环比）",
                "IMPORT_BASE_SEQUENTIAL": "当月进口额（环比）",
                "EXIT_ACCUMULATE": "累计出口额（亿美金）",
                "IMPORT_ACCUMULATE": "累计进口额（亿美金）",
                "EXIT_ACCUMULATE_SAME": "累计出口额（同比）",
                "IMPORT_ACCUMULATE_SAME": "累计进口额（同比）",
            }
        })
