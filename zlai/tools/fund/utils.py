# utils for https://fund.eastmoney.com/ data
import time
import random

__all__ = [
    "Constant",
    "get_current_timestamp",
    "jquery_mock_callback",
]


class Constant:
    jQuery_Version = "1.8.3"


def get_current_timestamp() -> int:
    return int(round(time.time() * 1000))


def jquery_mock_callback() -> str:
    return f'jQuery{(Constant.jQuery_Version + str(random.random())).replace(".", "")}_{str(get_current_timestamp() - 1000)}'
