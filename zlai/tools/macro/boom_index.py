from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "BoomIndexQueryConfig",
    "BoomIndex",
]


class BoomIndexQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BOOM_INDEX", "FAITH_INDEX", "BOOM_INDEX_SAME",
            "BOOM_INDEX_SEQUENTIAL", "FAITH_INDEX_SAME", "FAITH_INDEX_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_BOOM_INDEX",
            "_": self._current_time(),
        }
        return params


class BoomIndex(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[BoomIndexQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = BoomIndexQueryConfig.model_validate(kwargs)
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
            "description": "中国 企业景气及企业家信心指数",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "BOOM_INDEX": "企业景气指数",
                "FAITH_INDEX": "企业家信心指数",
                "BOOM_INDEX_SAME": "企业景气指数（同比）",
                "BOOM_INDEX_SEQUENTIAL": "企业景气指数（环比）",
                "FAITH_INDEX_SAME": "企业家信心指数（同比）",
                "FAITH_INDEX_SEQUENTIAL": "企业家信心指数（环比）",
            }
        })
