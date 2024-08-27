import unittest
from zlai.tools import *
from zlai.agent import Tools, ToolsAgent
from zlai.types.messages import UserMessage, TextContent
from zlai.llms import Zhipu, GLM4AllToolsGenerateConfig


class TestToolCall(unittest.TestCase):
    def test_tool_call(self):
        tool_list = [
            search_fund, get_fund_basic_info, get_current_fund,
            get_current_fund, get_fund_company, get_fund_history
        ]

        content = [TextContent(text="帮忙查询基金代码为008888的的名称、基金类型、基金拼音全称。")]
        content = "查询基金代码为008888的的名称、基金类型、基金拼音全称。"

        tools = Tools(tool_list=tool_list)
        llm = Zhipu(generate_config=GLM4AllToolsGenerateConfig(tools=tools.tool_descriptions, stream=True))
        completion = llm.generate(messages=[UserMessage(content=content)])
        for chunk in completion:
            print(chunk.choices[0].delta.tool_calls[0].function)
