from pydantic import BaseModel
from typing import Union

__all__ = [
    "BaseUrl",
    "ESUrl",
    "EMBUrl",
]


class BaseUrl(BaseModel):
    """"""
    def change_url_port(self, origin_port, new_port):
        """"""
        for field, value in self.model_dump().items():
            if isinstance(value, str) and value.startswith('http://'):
                setattr(self, field, value.replace(f':{origin_port}', f':{new_port}'))

    def apply_address(self, host: str, port: Union[int, str]):
        """"""
        for field, value in self.model_dump().items():
            if "port" in value:
                setattr(self, field, value.replace('port', port))
            if "host" in value:
                setattr(self, field, value.replace('host', host))


class EMBUrl(BaseUrl):
    # BGE
    bge_large: str = 'host:port/embedding/bge_large'
    bge_base: str = 'host:port/embedding/bge_base'
    bge_small: str = 'host:port/embedding/bge_small'
    bge_m3: str = 'host:port/embedding/bge_m3'
    # M3E
    m3e_large: str = 'host:port/embedding/m3e_large'
    m3e_base: str = 'host:port/embedding/m3e_base'
    m3e_small: str = 'host:port/embedding/m3e_small'


class ESUrl(BaseUrl):
    """"""
    url: str = "http://host:port/"
