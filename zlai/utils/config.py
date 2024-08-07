import os
import sys
import pathlib
from pydantic import BaseModel
from typing import Union, Tuple


__all__ = [
    "headers",
    "pkg_config",
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


class Config(BaseModel):
    cache_path: str = os.path.join(pathlib.Path.home(), ".zlai")
    python_version: Union[str, Tuple] = tuple(sys.version_info)


pkg_config = Config()


def create_pkg_cache_dir():
    """"""
    os.makedirs(pkg_config.cache_path, exist_ok=True)


create_pkg_cache_dir()
