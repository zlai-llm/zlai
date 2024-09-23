from typing import Any, Dict, List, Optional


__all__ = [
    "parse_mini_cpm_v3"
]


def parse_mini_cpm_v3(content: str, tokenizer: Any) -> Optional[List[Dict]]:
    """"""
    message = tokenizer.decode_function_call(content)
    return message.get("tool_calls")
