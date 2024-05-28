import re
import ast
import pandas as pd
from typing import Dict, List, Union, Tuple, Literal, Callable
from pydantic import BaseModel
from dataclasses import dataclass


__all__ = [
    "Re",
    "sparse_bool",
    "sparse_bool_lst",
    "sparse_list",
    "sparse_dict",
    "sparse_query",
    "sparse_markdown_table",
    # Sparse
    "ParseBase",
    "ParseDict",
    "ParseList",
    "ParseCode",
    "ParseString",
    "ParseMethod",
    "parse_method",
]

# TODO: LLM标签筛选机制

TypeScript = Literal["python", "sql", "json"]


@dataclass
class Re:
    """"""
    multi_space: str = r'\s+'


def sparse_bool(
        s: str,
) -> bool:
    """"""
    return eval(re.findall(r'\bTrue\b|\bFalse\b', s)[0])


def sparse_bool_lst(
        s: str,
) -> List[bool]:
    """"""
    bool_lst = [eval(item) for item in re.findall(r'\bTrue\b|\bFalse\b', s)]
    return bool_lst


def sparse_list(
        string: str,
        first: bool = True,
) -> Union[List[List], List, None]:
    """
    :param first:
    :param string:
    :return:
    """
    pattern = r'\[.*\]'
    matches = re.findall(pattern, string)
    lsts = []

    for match in matches:
        try:
            lst = ast.literal_eval(match)
            lsts.append(lst)
        except ValueError:
            pass
    if first:
        if len(lsts) > 0:
            return lsts[0]
        else:
            return None
    else:
        return lsts


def sparse_dict(
        string: str,
        first: bool = True,
) -> Union[List[Dict], Dict, None]:
    """
    :param first:
    :param string:
    :return:
    """
    pattern = r'\{.*\}'
    matches = re.findall(pattern, string)
    dicts = []

    for match in matches:
        try:
            dictionary = ast.literal_eval(match)
            dicts.append(dictionary)
        except ValueError:
            pass
    if first:
        if len(dicts) > 0:
            return dicts[0]
        else:
            return None
    else:
        return dicts


def sparse_markdown_table(
        text: str,
) -> pd.DataFrame:
    """
    :param text:
    :return:
    """
    split_md = text.split('\n')
    split_md = [line.strip().split("|")[1:-1] for line in split_md if len(line) > 0 and "----" not in line]
    split_md = [item for item in split_md if len(item) > 0]
    df = pd.DataFrame(split_md[1:], columns=split_md[0])
    return df


def sparse_query(
        string: str,
        query_type: str = "python",
) -> Union[None, str]:
    """"""
    pattern = fr"```{query_type}\n([\s\S]*?)```"
    matches = re.findall(pattern, string)
    if len(matches) > 0:
        return matches[0]
    else:
        return None


class ParseBase:
    """"""
    matches: List[str] = None
    sparse_error: List[Tuple] = []

    @classmethod
    def greedy_mark(
            cls,
            string: str,
            mark_pattern: str,
    ) -> Union[List[List], List[Dict]]:
        """
        解析 value 贪婪模式，寻找第一个 'mark' 到最后一个 'mark' 之间的内容，适用于文本中只有 1 个 mark content 的解析。
        :param mark_pattern:
        :param string:
        :return:
        """
        cls.matches = re.findall(mark_pattern, string, flags=re.DOTALL)
        values = []
        for match in cls.matches:
            try:
                value = ast.literal_eval(match)
                values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((match, f"Error: {error}"))
        return values

    @classmethod
    def eval_mark(
            cls,
            string: str,
            mark_pattern: str,
    ) -> Union[List[List], List[Dict]]:
        """
        解析 value 非贪婪模式，寻找任意 'mark' 之间 'mark' 之间的内容，适用于存在多个非嵌套模 value 的解析。
        :param mark_pattern:
        :param string:
        :return:

        example:
        """
        cls.matches = re.findall(mark_pattern, string, flags=re.DOTALL)
        values = []
        for match in cls.matches:
            try:
                value = ast.literal_eval(match)
                values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((match, f"Error: {error}"))
        return values

    @classmethod
    def nested_data(
            cls,
            string: str,
            mark: tuple = ("{", "}"),
    ) -> Union[List[List], List[Dict]]:
        """
        解析嵌套的 values，基本适用于全部情况的 value 解析。
        :param mark:
        :param string:
        :return:

        example:
        """
        stack = []
        nested_values_idx = []

        for i, char in enumerate(string):
            if char == mark[0]:
                stack.append(i)
            elif char == mark[1]:
                if stack:
                    left_bracket_index = stack.pop()
                    if len(stack) == 0:
                        nested_values_idx.append((left_bracket_index, i + 1))

        nested_values = []
        for (start, end) in nested_values_idx:
            try:
                value = ast.literal_eval(string[start: end])
                nested_values.append(value)
            except ValueError() as error:
                cls.sparse_error.append((string[start: end], f"Error: {error}"))
        return nested_values


class ParseList(ParseBase):
    """"""
    matches: List[str] = None
    pattern: str = r'\[.*?\]'
    greedy_pattern: str = r'\[.*\]'
    mark: Tuple[str] = ("[", "]")

    @classmethod
    def greedy_list(cls, string: str) -> List[List]:
        """"""
        return cls.greedy_mark(string=string, mark_pattern=cls.greedy_pattern)

    @classmethod
    def eval_list(cls, string: str) -> List[List]:
        """"""
        return cls.eval_mark(string=string, mark_pattern=cls.pattern)

    @classmethod
    def nested_list(cls, string: str) -> List[List]:
        """"""
        return cls.nested_data(string=string, mark=cls.mark)


class ParseDict(ParseBase):
    """"""
    matches: List[str] = None
    pattern: str = r'\{.*?\}'
    greedy_pattern: str = r'\{.*\}'
    # key_val_pattern = r"'([^']+)': '([^']*)'"
    key_val_pattern = r"['\"](\w+)['\"]:\s*['\"]([^'\"]+)['\"]"
    mark: Tuple[str] = ("{", "}")

    @classmethod
    def greedy_dict(cls, string: str, ) -> List[dict]:
        """
        解析dict贪婪模式，寻找第一个 '{' 到最后一个 '}' 之间的内容，适用于文本中只有 1 个字典的解析。
        :param string:
        :return:
        """
        return cls.greedy_mark(string=string, mark_pattern=cls.greedy_pattern)

    @classmethod
    def eval_dict(cls, string: str) -> List[Dict]:
        """
        解析dict非贪婪模式，寻找任意 '{' 之间 '}' 之间的内容，适用于存在多个非嵌套模型字典的解析。
        :param string:
        :return:

        example:

        """
        return cls.eval_mark(string=string, mark_pattern=cls.pattern)

    @classmethod
    def nested_dict(cls, string: str) -> List[Dict]:
        """
        解析嵌套的 dict，基本适用于全部情况的字典解析。
        :param string:
        :return:

        example:

        """
        return cls.nested_data(string=string, mark=cls.mark)

    @classmethod
    def key_value_dict(cls, string: str) -> List[Dict]:
        """
        todo: 还需要考虑单引号、双引号、还有多行识别未解决，有点麻烦
        依据冒号对 key-value 提取。
        :param string:
        :return:
        """
        tuple_data = re.findall(cls.key_val_pattern, string)
        return [dict(tuple_data)]


class ParseCode:
    """"""
    @classmethod
    def sparse_script(
            cls,
            string: str,
            script: TypeScript = "python",
    ) -> List[str]:
        """"""
        pattern = fr"```{script}\n([\s\S]*?)```"
        matches = re.findall(pattern, string)
        if len(matches) > 0:
            matches = [match[:-1] if match.endswith('\n') else match for match in matches]
        return matches


class ParseString(ParseDict, ParseList, ParseCode):
    """
    parse class.
    """
    
    @classmethod
    def warp_udf_parse(cls, *args, **kwargs) -> Callable:
        """"""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                data = None
                try:
                    data = func(*args, **kwargs)
                except Exception as error:
                    cls.sparse_error.append((f"args: {args}. kwargs: {kwargs}", f"Error: {error}."))
                return data
            return wrapper
        return decorator

    @classmethod
    def udf_parse(cls, func: Callable, content, **kwargs) -> str:
        """"""
        data = None
        try:
            data = func(content, **kwargs)
        except Exception as error:
            cls.sparse_error.append((f"kwargs: {kwargs}", f"Error: {error}."))
        return data


class ParseMethod(BaseModel):
    """"""
    # list
    greedy_list: Callable = ParseString.greedy_list
    eval_list: Callable = ParseString.eval_list
    nested_list: Callable = ParseString.nested_list

    # dict
    greedy_dict: Callable = ParseString.greedy_dict
    eval_dict: Callable = ParseString.eval_dict
    nested_dict: Callable = ParseString.nested_dict


parse_method = ParseMethod().model_dump()

