from typing import Any, List, Dict, Union, Callable
from ..schema import CompletionMessage
from ..parse import *


__all__ = [
    "warp_sparse_eval_dict",
    "warp_sparse_nested_dict",
    "warp_sparse_greedy_dict",
    "warp_sparse_eval_list",
    "warp_sparse_nested_list",
    "warp_sparse_greedy_list",
]


def validate_dtype_and_get_message_content(
        message: Union[CompletionMessage, str]
) -> str:
    """"""
    if isinstance(message, str):
        content = message
    elif isinstance(message, CompletionMessage):
        content = message.content
    else:
        raise ValueError(f"Unsupported message type: {type(message)}")
    return content


def create_warp_output(
        message: Union[CompletionMessage, str],
        data: Union[List[dict], List[List]],
) -> Union[CompletionMessage, List[Dict], List[List]]:
    """"""
    if isinstance(message, str):
        return data
    elif isinstance(message, CompletionMessage):
        message.content = data
        data = message
        return data
    else:
        raise ValueError(f"Unsupported message type: {type(message)}")


def warp_sparse_eval_dict(func: Callable) -> Callable:
    """TODO: 是否还需要增加输入的数据类型？"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.eval_dict(string=content)
        data = create_warp_output(message, data)
        return data
    return wrapper


def warp_sparse_nested_dict(func: Callable, ) -> Callable:
    """"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.nested_dict(string=content)
        data = create_warp_output(message, data)
        return data

    return wrapper


def warp_sparse_greedy_dict(func: Callable, ) -> Callable:
    """"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.greedy_dict(string=content)
        data = create_warp_output(message, data)
        return data

    return wrapper


def warp_sparse_eval_list(func: Callable) -> Callable:
    """TODO: 是否还需要增加输入的数据类型？"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.eval_list(string=content)
        data = create_warp_output(message, data)
        return data

    return wrapper


def warp_sparse_nested_list(func: Callable, ) -> Callable:
    """"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.nested_list(string=content)
        data = create_warp_output(message, data)
        return data

    return wrapper


def warp_sparse_greedy_list(func: Callable, ) -> Callable:
    """"""
    sparse = ParseString()

    def wrapper(*args, **kwargs) -> Union[CompletionMessage, List[Dict]]:
        """"""
        message: Union[CompletionMessage, str] = func(*args, **kwargs)
        content = validate_dtype_and_get_message_content(message)
        data = sparse.greedy_list(string=content)
        data = create_warp_output(message, data)
        return data

    return wrapper
