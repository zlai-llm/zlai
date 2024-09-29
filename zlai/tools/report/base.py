import time
import requests
from pydantic import BaseModel
from typing import Dict, Optional
from zlai.tools.utils import headers
from zlai.utils.mixin import LoggerMixin


__all__ = [
    "assemble_url",
    "BaseRequestConfig",
    "BaseRequestData",
]


def assemble_url(base_url: str, params: Dict) -> str:
    """"""
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    request_url = f"{base_url}?{query_string}"
    return request_url


class BaseRequestConfig(BaseModel):
    """"""
    def _current_time(self) -> str:
        """"""
        return str(int(time.time() * 1E3))

    def to_params(self) -> Dict:
        """"""
        return dict()


class BaseRequestData(LoggerMixin):
    """"""
    query_config: Optional[BaseRequestConfig]

    def _base_url(self) -> str:
        """"""
        return ""

    def request_json(self) -> Dict:
        """"""
        base_url = self._base_url()
        params = self.query_config.to_params()
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        return data
