from enum import Enum
from copy import deepcopy
from typing import Annotated, List, Dict
from .agent import register_tool, dispatch_tool
from ..llms import *
from ..elasticsearch import *


__all__ = [
    "get_policy_tools",
    "policy_tools",
]


POLICY_TOOL_HOOKS = {}
POLICY_TOOL_DESCRIPTIONS = []


class PolicyIndex(str, Enum):
    """"""
    punish = Annotated[str, "处罚文本库", "punish"]
    policy = Annotated[str, "政策文本库", "policy"]


@register_tool(tool_hooks=POLICY_TOOL_HOOKS, tool_descriptions=POLICY_TOOL_DESCRIPTIONS)
def get_policy(
        key_word: Annotated[str, '用户传入的关键词', True],
        size: Annotated[int, '返回文档的数量，默认为5', False] = 5,
        index_name: Annotated[PolicyIndex, 'ElasticSearch索引名称', False] = 'test_index',
) -> List[Dict[str, str]]:
    """
    依据用户传入的问题关键词，通过相似度计算返回最相近的政策文件。
    """
    vector = emb(url=emb_url.m3e_large, text=key_word)

    con = get_es_con(hosts=ESUrl.model)
    tools = ElasticSearchTools(index_name=index_name, con=con)
    tools.cos_smi(vector)
    data = tools.execute(size=size)
    return [item.get("_source") for item in data]


def get_policy_tools() -> List[Dict]:
    """"""
    return deepcopy(POLICY_TOOL_DESCRIPTIONS)


def policy_tools(
        tool_name: str,
        tool_params: dict,
) -> str:
    """"""
    return dispatch_tool(tool_name=tool_name, tool_params=tool_params, hooks=POLICY_TOOL_HOOKS)
