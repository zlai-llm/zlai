import time
import requests
from pydantic import BaseModel, Field
from typing import Any, Dict, Union, Callable, Optional
from zlai.utils.mixin import LoggerMixin
from zlai.tools.utils import headers
from zlai.types.tools import ResponseData
from .base import *


__all__ = [
    "ProfitForecast"
]


class ProfitForecastConfig(BaseModel):
    """"""
    size: Optional[int] = Field(default=5, description="数据量")
    code: Optional[Union[str, int]] = Field(default=None, description="股票代码")
    industry: Optional[str] = Field(default=None, description="行业板块")
    district: Optional[str] = Field(default=None, description="地域板块")
    conception: Optional[str] = Field(default=None, description="概念板块")

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def _query_condition(self) -> str:
        """"""
        if self.code:
            condition = f'(SECURITY_CODE="{self.code}")'
        elif self.industry:
            condition = f'(INDUSTRY_BOARD="{self.industry}")'
        elif self.district:
            condition = f'(REGION_BOARD="{self.district}")'
        elif self.conception:
            condition = f'(CONCEPTINDEX_BOARD+like"%{self.conception}%")'
        else:
            condition = ""
        return condition

    def to_params(self) -> Dict:
        """"""
        params = {
            "reportName": "RPT_WEB_RESPREDICT",
            "columns": "WEB_RESPREDICT",
            "pageNumber": "1",
            "pageSize": self.size,
            "sortTypes": "-1",
            "sortColumns": "RATING_ORG_NUM",
            "filter": self._query_condition(),
            "p": "1",
            "pageNo": "1",
            "pageNum": "1",
            "_": str(int(time.time() * 1E3)),
        }
        return params


class ProfitForecast(LoggerMixin):
    """"""
    def __init__(
            self,
            query_config: Optional[ProfitForecastConfig] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        """"""
        if query_config is None:
            self.query_config = ProfitForecastConfig.model_validate(kwargs)
        else:
            self.query_config = query_config
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs

    def load_data(self, ) -> ResponseData:
        """"""
        base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = self.query_config.to_params()
        response = requests.get(base_url, params=params, headers=headers)
        metadata = response.json().get("result", {})
        data = metadata.pop("data")
        self.update_metadata(metadata)
        self._logger(msg=f"[{__class__.__name__}] Find {len(data)} reports.", color="green")
        return ResponseData(data=data, metadata=metadata)

    def update_metadata(self, metadata: Dict):
        """"""
        metadata.update({
            "description": "机构盈利预测",
            "columns": {
                "SECUCODE": "股票代码",
                "SECURITY_CODE": "证券代码",
                "SECURITY_NAME_ABBR": "证券简称",
                "RATING_ORG_NUM": "评级机构数量",
                "RATING_BUY_NUM": "买入评级数量",
                "RATING_ADD_NUM": "增持评级数量",
                "RATING_NEUTRAL_NUM": "中性评级数量",
                "RATING_REDUCE_NUM": "减持评级数量",
                "RATING_SALE_NUM": "卖出评级数量",
                "YEAR1": "第一年",
                "YEAR_MARK1": "第一年标记",
                "EPS1": "第一年每股收益",
                "YEAR2": "第二年",
                "YEAR_MARK2": "第二年标记",
                "EPS2": "第二年每股收益",
                "YEAR3": "第三年",
                "YEAR_MARK3": "第三年标记",
                "EPS3": "第三年每股收益",
                "YEAR4": "第四年",
                "YEAR_MARK4": "第四年标记",
                "EPS4": "第四年每股收益",
                "INDUSTRY_BOARD": "行业板块",
                "INDUSTRY_BOARD_SZM": "深证行业板块",
                "CONCEPTINDEX_BOARD": "概念指数板块",
                "CONCEPTINDEX_BOARD_SZM": "深证概念指数板块",
                "REGION_BOARD": "区域板块",
                "REGION_BOARD_SZM": "深证区域板块",
                "MARKET_BOARD": "市场板块",
                "DEC_AIMPRICEMAX": "目标最高价",
                "DEC_AIMPRICEMIN": "目标最低价",
                "RATING_LONG_NUM": "长期评级数量",
            }
        })
