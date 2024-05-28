import os
import re
import json
import inspect
from typing import List, Dict, Any, Type, Callable, Optional
import chardet
import numpy as np
from dataclasses import dataclass
from termcolor import colored

__all__ = [
    "batches",
    "call_batches",
    "get_file_encoding",
    "split_multi_mark",
    "label_by_smi",
    "load_folder_file",
    "append_dict_to_json",
    "yield_string",
    "find_message",
    "get_next_message",
    "log",
    "get_dataclass_metadata",
    "get_dataclas_values",
    "get_dataclas_keys",
    "is_method_of_class",
]


def get_file_encoding(
        file_path: str
) -> str:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result.get('encoding')


def split_multi_mark(
        s: str,
        split: List[str] = []
) -> List[str]:
    """
    desc: 文本切分
    :param s:
    :param split:
    :return:
    """
    pattern = f"[{''.join(split)}]+"
    if len(pattern) > 3:
        parts = re.split(pattern, s)
        return parts
    else:
        return [s]


def label_by_smi(
        metrix: np.array,
        low: float = 0.3,
        upper: float = 0.7,
        top: int = 1,
        labels: List[str] = [],
        axis: int = 0,
) -> List[str]:
    """
    desc: 依据相似度矩阵选择标签
    :param axis: metrix的求和轴
    :param metrix: 相似度矩阵
    :param low: 最小相似度值
    :param upper: 最大相似度值
    :param top: 是否在不满足最大相似度时取 top-n
    :param labels: 标签
    :return: List[str]
    """
    match_label = []

    if np.size(metrix) == 0:
        return match_label

    labels_smi = metrix.max(axis=axis)

    if len(labels_smi) != len(labels):
        raise ValueError(f"sim: {len(labels_smi)} != label: {len(labels)}")

    if labels_smi.max() < low:
        return match_label
    elif labels_smi.max() >= upper:
        match_label = [label for label, sim in zip(labels, labels_smi) if sim >= upper]
        return match_label
    else:
        if top:
            return [labels[labels_smi.argmax()]]
        else:
            return []


def batches(
        lst: list,
        batch_size: int,
) -> List:
    """
    desc: 生成批次数据
    :param lst: 原始List
    :param batch_size: 批次大小
    :return:
    """
    for i in range(0, len(lst), batch_size):
        yield lst[i:i+batch_size]


def load_folder_file(
        path: str,
        endwith: str = '.txt',
        encoding: str = 'utf-8',
) -> List[Dict]:
    """
    desc: 加载文件夹下所有文件
    :param path:
    :param endwith:
    :param encoding:
    :return:
    """
    file_list = [file for file in os.listdir(path) if file.endswith(endwith)]
    file_content = []
    for file in file_list:
        file_path = os.path.join(path, file)
        with open(file_path, 'r', encoding=encoding) as f:
            data = f.read()
        file_content.append({
            "file": file, "data": data})
    return file_content


def find_message(data: Dict, file_path: str,) -> bool:
    """"""
    with open(file_path, 'r') as file:
        existing_data = json.load(file)
    if data in existing_data:
        return True
    else:
        return False


def get_next_message(data: Dict, file_path: str,) -> Dict:
    """"""
    with open(file_path, 'r') as file:
        existing_data = json.load(file)

    next_id = existing_data.index(data) + 1
    return existing_data[next_id]


def append_dict_to_json(
        data: Dict,
        file_path: str,
        max_records: int = 1000,
):
    """
    :param data:
    :param file_path:
    :param max_records:
    :return:
    """
    with open(file_path, 'r') as file:
        existing_data = json.load(file)

    existing_data.append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data[-max_records:], file)


def yield_string(string):
    """"""
    for i in range(len(string)):
        yield string[: i + 1]
    return string


def log(text, color='green'):
    """"""
    print(colored(text, color))


def get_dataclass_metadata(cls):
    """
    Get the metadata of a dataclass
    :param cls:
    :return:
    """
    metadata = dict()
    for key, val in cls.__dataclass_fields__.items():
        metadata.update({val.default: key})
    return metadata


def get_dataclas_values(cls: dataclass) -> List[Any]:
    """
    Get the values of a dataclass
    :param cls:
    :return:
    """
    return [val.default for key, val in cls.__dataclass_fields__.items()]


def get_dataclas_keys(cls: dataclass) -> List[str]:
    """
    Get the keys of a dataclass
    :param cls:
    :return:
    """
    return [key for key, val in cls.__dataclass_fields__.items()]


def is_method_of_class(func: Callable, cls: Type) -> bool:
    """"""
    if inspect.ismethod(func):
        return func.__self__.__class__ == cls
    elif inspect.isfunction(func):
        return getattr(func, "__qualname__", "").startswith(cls.__name__ + ".")
    else:
        return False


def call_batches(
        batch_size: int,
        data: Optional[List] = None,
        data_len: Optional[int] = None,

) -> int:
    """"""
    if data:
        data_len = len(data)
    elif data_len is None:
        raise ValueError("Either data or data_len must be provided.")
    if data_len // batch_size == data_len / batch_size:
        total = data_len // batch_size
    else:
        total = (data_len // batch_size) + 1
    return total
