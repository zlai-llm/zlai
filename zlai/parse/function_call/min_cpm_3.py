from typing import Any, Dict, List, Optional


__all__ = [
    "parse_mini_cpm_v3"
]


def parse_mini_cpm_v3(content: str, tokenizer: Any, **kwargs) -> Optional[List[Dict]]:
    """"""
    message = tokenizer.decode_function_call(content)
    tool_calls = message.get("tool_calls")
    if tool_calls is not None:
        functions = [tool_call.get("function") for tool_call in tool_calls]
    else:
        functions = None
    return functions
