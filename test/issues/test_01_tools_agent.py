import unittest
from zlai.llms import Zhipu, GLM4AirGenerateConfig, GLM40520GenerateConfig, GLM4FlashGenerateConfig
from zlai.agent.tools import *


class TestToolsAgent(unittest.TestCase):
    """"""
    def test_issue_01(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())
        tools = Tools(tool_list=[get_weather, random_number_generator])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("输出一个0-6的随机数？")
        print(task_completion.content)


