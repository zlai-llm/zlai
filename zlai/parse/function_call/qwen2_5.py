from typing import List, Dict, Callable, Optional
from .base import parse_dict_content


__all__ = [
    "parse_qwen2_5"
]


def _parse(func: List[Callable], content: List[str]) -> Optional[Dict]:
    """"""
    for f, c in zip(func, content):
        try:
            f_data = f(c)
            return f_data
        except Exception as e:
            continue
    return None


def parse_qwen2_5(content: str, tools_name: List[str], **kwargs) -> Optional[List[Dict]]:
    """"""
    functions = None
    keywords = ["name", "arguments", "{", "}"]
    mark = all([item in content for item in keywords])
    if mark:
        content = parse_dict_content(content)
        function_json = _parse(
            func=[eval, eval],
            content=[content, content[1: -1]],
        )
        if function_json is not None:
            name = function_json.get("name")
            arguments = str(function_json.get("arguments"))
            if name in tools_name:
                functions = [{"name": name, "arguments": arguments}]
    return functions
