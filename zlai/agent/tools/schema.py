from pydantic import BaseModel, Field
from typing import Dict, List


__all__ = [
    "ToolParameters",
    "ToolFunction",
    "ToolItem",
    "WebSearch",
    "ToolWebSearch",
]


class ToolParameters(BaseModel):
    """"""
    type: str = "object"
    properties: Dict[str, Dict]
    required: List[str]


class ToolFunction(BaseModel):
    """"""
    name: str
    description: str
    parameters: ToolParameters


class ToolItem(BaseModel):
    type: str = "function"
    function: ToolFunction


class WebSearch(BaseModel):
    """"""
    enable: bool = Field(default=True, description="是否启用搜索，默认启用搜索 启用：true 禁用：false")
    search_query: str = Field(default=None, description="强制搜索自定义关键内容，此时模型会根据自定义搜索关键内容返回的结果作为背景知识来回答用户发起的对话。")
    search_result: bool = Field(default=False, description="获取详细的网页搜索来源信息，包括来源网站的图标、标题、链接、来源名称以及引用的文本内容。默认为关闭。 启用：true 禁用：false")


class ToolWebSearch(BaseModel):
    """"""
    type: str = "web_search"
    web_search: WebSearch
