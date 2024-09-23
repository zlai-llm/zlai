from typing import List, Dict, Optional


__all__ = [
    "parse_glm4"
]


def parse_glm4(
        content: str,
        tools_name: List[str],
        **kwargs
) -> Optional[List[Dict]]:
    """"""
    functions = None
    lines = content.strip().split("\n")
    if len(lines) >= 2 and lines[1].startswith("{"):
        name, arguments = lines[0].strip(), "\n".join(lines[1:]).strip()

        try:
            arguments = eval(arguments)
        except Exception as e:
            return functions

        if name in tools_name:
            functions = [{"name": name, "arguments": arguments}]
            return functions
        else:
            return functions
    return functions
