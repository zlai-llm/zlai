from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "PMIQueryConfig",
    "PMI",
]


class PMIQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """"""
        columns = [
            "REPORT_DATE", "TIME", "MAKE_INDEX", "MAKE_SAME", "NMAKE_INDEX", "NMAKE_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_PMI",
            "_": self._current_time(),
        }
        return params


class PMI(BaseRequestData):
    """采购经理人指数(PMI)"""
    def __init__(
            self,
            query_config: Optional[PMIQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = PMIQueryConfig.model_validate(kwargs)
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
        中国 采购经理人指数(PMI)
        :return:
        """
        metadata = self.request_json().get("result", {})
        data = metadata.pop("data")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """中国 采购经理人指数(PMI)"""
        metadata.update({
            "description": "中国 采购经理人指数(PMI)",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "MAKE_INDEX": "制造业指数",
                "MAKE_SAME": "制造业同比增长",
                "NMAKE_INDEX": "非制造业指数",
                "NMAKE_SAME": "非制造业同比增长",
            }
        })
