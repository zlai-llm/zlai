from pydantic import BaseModel
from typing import Dict


__all__ = [
    "config",
]


class Config(BaseModel):
    """"""
    headers: Dict = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Referer': 'https://fundf10.eastmoney.com/',
    }


config = Config()
