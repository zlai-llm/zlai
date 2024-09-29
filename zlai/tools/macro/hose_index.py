from pydantic import Field
from typing import Any, List, Dict, Callable, Optional
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "HoseIndexOldQueryConfig",
    "HoseIndexOld",
    "HoseIndexNewQueryConfig",
    "HoseIndexNew",
]


class HoseIndexOldQueryConfig(BaseRequestConfig):
    """"""
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "TIME", "HOSE_INDEX", "HOSE_INDEX_SAME", "LAND_INDEX",
            "LAND_INDEX_SAME", "GOODSHOSE_INDEX", "GOODSHOSE_INDEX_SAME"
        ]
        params = {
            "columns": ",".join(columns),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_HOSE_INDEX",
            "_": self._current_time(),
        }
        return params


class HoseIndexOld(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[HoseIndexOldQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        if query_config is None:
            self.query_config = HoseIndexOldQueryConfig.model_validate(kwargs)
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
            "description": "中国 房价指数(08—10年)",
            "columns": {
                "REPORT_DATE": "报告日期",
                "TIME": "时间",
                "HOSE_INDEX": "国房景气指数（指数值）",
                "HOSE_INDEX_SAME": "国房景气指数（同比增长）",
                "LAND_INDEX": "土地开发面积指数（指数值）",
                "LAND_INDEX_SAME": "土地开发面积指数（指数值）",
                "GOODSHOSE_INDEX": "销售价格指数（同比增长）",
                "GOODSHOSE_INDEX_SAME": "销售价格指数（同比增长）",
            }
        })


class HoseIndexNewQueryConfig(BaseRequestConfig):
    """"""
    cities: Optional[List[str]] = Field(default=["北京", "上海"])
    report_date: Optional[str] = Field(default=None)
    size: Optional[int] = Field(default=20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _data_filter(self):
        """"""
        if self.report_date:
            _filter = f"(REPORT_DATE='{self.report_date}')"
        elif self.cities:
            cities = [f'"{item}"' for item in self.cities]
            _filter = f'(CITY+in+({",".join(cities)}))'
        else:
            raise ValueError("report_date or cities must be set")
        return _filter

    def to_params(self) -> Dict:
        """
        :return:
        """
        columns = [
            "REPORT_DATE", "CITY", "FIRST_COMHOUSE_SAME", "FIRST_COMHOUSE_SEQUENTIAL",
            "FIRST_COMHOUSE_BASE", "SECOND_HOUSE_SAME", "SECOND_HOUSE_SEQUENTIAL",
            "SECOND_HOUSE_BASE", "REPORT_DAY"
        ]

        params = {
            "columns": ",".join(columns),
            "filter": self._data_filter(),
            "pageNumber": "1",
            "pageSize": self.size,
            "sortColumns": "REPORT_DATE,CITY",
            "sortTypes": "-1,-1",
            "source": "WEB",
            "client": "WEB",
            "reportName": "RPT_ECONOMY_HOUSE_PRICE",
            "_": self._current_time(),
        }
        return params


class HoseIndexNew(BaseRequestData):
    """"""
    def __init__(
            self,
            query_config: Optional[HoseIndexNewQueryConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """

        :param query_config:
        :param cities: 城市
        :param size: 数据量
        :param report_date: 日期
        :param verbose:
        :param logger:
        :param kwargs:
        """
        if query_config is None:
            self.query_config = HoseIndexNewQueryConfig.model_validate(kwargs)
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
            "description": "中国 新房价指数",
            "columns": {
                "REPORT_DATE": "时间",
                "CITY": "城市",
                "FIRST_COMHOUSE_SAME": "新建商品住宅价格指数（同比）",
                "FIRST_COMHOUSE_SEQUENTIAL": "新建商品住宅价格指数（环比）",
                "FIRST_COMHOUSE_BASE": "新建商品住宅价格指数（定基）",
                "SECOND_HOUSE_SAME": "二手住宅价格指数（同比）",
                "SECOND_HOUSE_SEQUENTIAL": "二手住宅价格指数（环比）",
                "SECOND_HOUSE_BASE": "二手住宅价格指数（定基）",
                "REPORT_DAY": "日期",
            }
        })
