from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "DepositReserveQueryConfig",
    "DepositReserve",
]


class DepositReserveQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "PUBLISH_DATE", "TRADE_DATE", "INTEREST_RATE_BB", "INTEREST_RATE_BA",
            "CHANGE_RATE_B", "INTEREST_RATE_SB", "INTEREST_RATE_SA", "CHANGE_RATE_S", "NEXT_SH_RATE",
            "NEXT_SZ_RATE", "REMARK",
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "PUBLISH_DATE,TRADE_DATE",
            "sortTypes": "-1,-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_DEPOSIT_RESERVE",
            "_": self._current_time(),
        }
        return params


class DepositReserve(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[DepositReserveQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = DepositReserveQueryConfig.model_validate(kwargs)
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
            "description": "中国 存款准备金率",
            "columns": {
                "REPORT_DATE": "报告时间",
                "PUBLISH_DATE": "公布时间",
                "TRADE_DATE": "生效时间",
                "INTEREST_RATE_BB": "大型金融机构（调整前）",
                "INTEREST_RATE_BA": "大型金融机构（调整后）",
                "CHANGE_RATE_B": "大型金融机构（调整幅度）",
                "INTEREST_RATE_SB": "中小金融机构（调整前）",
                "INTEREST_RATE_SA": "中小金融机构（调整后）",
                "CHANGE_RATE_S": "中小金融机构（调整幅度）",
                "NEXT_SH_RATE": "消息公布次日指数涨跌（上证-SH）",
                "NEXT_SZ_RATE": "消息公布次日指数涨跌（深证-SZ）",
                "REMARK": "消息",
            }
        })
