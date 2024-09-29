from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "DepositRateQueryConfig",
    "DepositRate",
]


class DepositRateQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "PUBLISH_DATE", "DEPOSIT_RATE_BB", "DEPOSIT_RATE_BA", "DEPOSIT_RATE_B", "LOAN_RATE_SB",
            "LOAN_RATE_SA", "LOAN_RATE_S", "NEXT_SH_RATE", "NEXT_SZ_RATE",
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_DEPOSIT_RATE",
            "_": self._current_time(),
        }
        return params


class DepositRate(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[DepositRateQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = DepositRateQueryConfig.model_validate(kwargs)
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
            "description": "中国 利率调整",
            "columns": {
                "REPORT_DATE": "公布时间",
                "PUBLISH_DATE": "生效时间",
                "DEPOSIT_RATE_BB": "存款基准利率(调整前)",
                "DEPOSIT_RATE_BA": "存款基准利率(调整后)",
                "DEPOSIT_RATE_B": "存款基准利率(调整幅度)",
                "LOAN_RATE_SB": "贷款基准利率(调整前)",
                "LOAN_RATE_SA": "贷款基准利率(调整后)",
                "LOAN_RATE_S": "贷款基准利率(调整幅度)",
                "NEXT_SH_RATE": "消息公布次日指数涨跌(SH)",
                "NEXT_SZ_RATE": "消息公布次日指数涨跌(SZ)",
            }
        })
