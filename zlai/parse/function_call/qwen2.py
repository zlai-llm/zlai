from typing import List, Dict, Optional
from zlai.parse import ParseDict


__all__ = [
    "parse_qwen2"
]


def parse_qwen2(
        content: str,
        tools_name: List[str],
        **kwargs
) -> Optional[List[Dict]]:
    """"""
    functions = None
    if "name" in content and "arguments" in content:
        function_json = None
        try:
            function_json = eval(content)
        except TypeError as e:
            function_json = eval(content[1: -1])
        except SyntaxError as e:
            function_json = ParseDict.greedy_dict(string=content)[0]
        finally:
            if function_json is not None:
                name = function_json.get("name")
                arguments = str(function_json.get("arguments"))
                if name in tools_name:
                    functions = [{"name": name, "arguments": arguments}]
    return functions
