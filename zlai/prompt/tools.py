from typing import *
from ..schema import ToolsPrompt, SystemPrompt


__all__ = [
    "tool_content",
    "get_base_tool_prompt",
    "get_base_system_prompt",
]


tool_content = """你是一个政策解读专家:
"""


def get_base_tool_prompt(
        tools: Union[List[Dict], Dict, None] = None,
        content: Union[str, None] = None,
) -> ToolsPrompt:
    """"""
    if content is None:
        content = "Answer the following questions as best as you can. You have access to the following tools:"
    base_tool_prompt = ToolsPrompt(role='system', content=content, tools=tools)
    return base_tool_prompt


def get_base_system_prompt(
    content: Union[str, None] = None,
) -> SystemPrompt:
    if content is None:
        content = "Answer the following questions as best as you can."
    base_system_prompt = SystemPrompt(role='system', content=content)
    return base_system_prompt

