from pydantic import Field
from typing import Any, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "GoodsIndexQueryConfig",
    "GoodsIndex",
]


class GoodsIndexQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "BASE", "BASE_SAME", "BASE_SEQUENTIAL", "FARM_BASE", "FARM_BASE_SAME",
            "FARM_BASE_SEQUENTIAL", "MINERAL_BASE", "MINERAL_BASE_SAME", "MINERAL_BASE_SEQUENTIAL", "ENERGY_BASE",
            "ENERGY_BASE_SAME", "ENERGY_BASE_SEQUENTIAL"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_GOODS_INDEX",
            "_": self._current_time(),
        }
        return params


class GoodsIndex(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[GoodsIndexQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = GoodsIndexQueryConfig.model_validate(kwargs)
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
            "description": "中国 企业商品价格指数",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "BASE": "总指数",
                "BASE_SAME": "总指数（同比）",
                "BASE_SEQUENTIAL": "总指数（环比）",
                "FARM_BASE": "农产品",
                "FARM_BASE_SAME": "农产品（同比）",
                "FARM_BASE_SEQUENTIAL": "农产品（环比）",
                "MINERAL_BASE": "矿产品",
                "MINERAL_BASE_SAME": "矿产品（同比）",
                "MINERAL_BASE_SEQUENTIAL": "矿产品（环比）",
                "ENERGY_BASE": "煤油电",
                "ENERGY_BASE_SAME": "煤油电（同比）",
                "ENERGY_BASE_SEQUENTIAL": "煤油电（环比）",
            }
        })
