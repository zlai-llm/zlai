import time
import requests
from typing import Dict
from zlai.utils.mixin import *
from zlai.tools.utils import headers
from zlai.types.tools import ResponseData


__all__ = [
    "ReportMapping"
]


class ReportMapping(LoggerMixin):
    """"""
    base_url: str = "https://reportapi.eastmoney.com/report/bk"
    mapping_code: Dict[str, str] = {
        "地域板块": "020",
        "行业板块": "016",
        "概念板块": "007",
    }

    def _get_data(self, params: Dict) -> ResponseData:
        """"""
        response = requests.get(self.base_url, params=params, headers=headers)
        metadata = response.json()
        data = metadata.pop("data")
        return ResponseData(data=data, metadata=metadata)

    def list_industry(self, ) -> ResponseData:
        """"""
        params = {"bkCode": "016", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_conception(self) -> ResponseData:
        """"""
        params = {"bkCode": "020", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)

    def list_district(self) -> ResponseData:
        """"""
        params = {"bkCode": "007", "_": str(int(time.time() * 1E3))}
        return self._get_data(params)
