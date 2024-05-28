import re
from typing import List, Union


__all__ = [
    "sparse_amount",
    "sparse_values",
]


def sparse_amount(amount_list: List[str]) -> List[Union[None, float]]:
    """"""
    pattern = r"(\d+(?:\.\d+)?)元$|(\d+(?:\.\d+)?)万元$|(\d+(?:\.\d+)?)亿元$"

    def mapping_pattern(item: str):
        """"""
        match = re.search(pattern, item)
        if match:
            if match.group(1):
                value = float(match.group(1))
            elif match.group(2):
                value = float(match.group(2)) * 1e4
            else:
                value = float(match.group(3)) * 1e8
        else:
            value = None
        return value

    amt_lst = list(map(mapping_pattern, amount_list))
    return amt_lst


def sparse_values(str_list: List[str]) -> List[float]:
    """"""
    pattern = r"(-?\d+(?:\.\d+)?)"

    def mapping_pattern(item: str):
        match = re.search(pattern, item)
        if match:
            value = float(match.group(0))
        else:
            value = None
        return value
    float_list = list(map(mapping_pattern, str_list))
    return float_list
