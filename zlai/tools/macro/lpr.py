from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "LPRQueryConfig",
    "LPR",
]


class LPRQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "TRADE_DATE", "LPR1Y", "LPR5Y", "RATE_1", "RATE_2"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "TRADE_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPTA_WEB_RATE",
            "_": self._current_time(),
        }
        return params


class LPR(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[LPRQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = LPRQueryConfig.model_validate(kwargs)
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
            "description": "中国 LPR品种详细数据",
            "columns": {
                "TRADE_DATE": "日期",
                "LPR1Y": "LPR_1Y利率(%)",
                "LPR5Y": "LPR_5Y利率(%)",
                "RATE_1": "短期贷款利率:6个月至1年(含)(%)",
                "RATE_2": "中长期贷款利率:5年以上(%)",
            }
        })
