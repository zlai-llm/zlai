from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "TaxQueryConfig",
    "Tax",
]


class TaxQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "TAX_INCOME", "TAX_INCOME_SAME", "TAX_INCOME_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_TAX",
            "_": self._current_time(),
        }
        return params


class Tax(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[TaxQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = TaxQueryConfig.model_validate(kwargs)
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
            "description": "中国 全国税收收入",
            "columns": {
                "START_DATE": "开始时间",
                "END_DATE": "截至时间",
                "TAX_INCOME": "税收收入合计(亿元)",
                "TAX_INCOME_SAME": "较上年同期(%)",
                "TAX_INCOME_SEQUENTIAL": "季度环比(%)",
            }
        })
