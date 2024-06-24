import unittest
from zlai.agent.tools import *
from zlai.llms import Zhipu, GLM4FlashGenerateConfig


class TestTools(unittest.TestCase):
    """"""

    def test_params(self):
        """"""
        tool_hooks = {}
        tool_descriptions = []
        register_tool(tool_hooks=tool_hooks, tool_descriptions=tool_descriptions)(random_number_generator)
        register_tool(tool_hooks=tool_hooks, tool_descriptions=tool_descriptions)(get_weather)
        print(tool_hooks)
        print(tool_descriptions)
        print(get_weather)

    def test_tools(self):
        """"""
        tools = Tools(function_list=[get_weather])
        print(tools)
        print(tools.function_list[0]("杭州"))
        input_ = {"tool_name": "get_weather", "tool_params": {"city_name": "杭州"}}
        print(tools.dispatch_tool(**input_))

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())

        tools = Tools(function_list=[get_weather, random_number_generator])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("输出一个0-6的随机数？")
        print(task_completion.content)
