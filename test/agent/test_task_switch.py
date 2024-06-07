import unittest
from zlai.llms import Zhipu, GLM4FlashGenerateConfig
from zlai.agent import TaskSwitch, TaskDescription, ChatAgent, Weather


class TestTaskSwitch(unittest.TestCase):
    """"""
    def setUp(self):
        """"""

    def test_task_switch(self):
        """"""
        task_switch_list = [
            TaskDescription(
                task=ChatAgent, task_id=0, task_name="闲聊机器人",
                task_description="""解答用户的各类闲聊问题""",
            ),
            TaskDescription(
                task=Weather, task_id=1, task_name="天气播报机器人",
                task_description="""查询当前的天气数据，并为用户播报当前的天气信息""",
            ),
        ]

        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())
        chat = TaskSwitch(llm=llm, task_list=task_switch_list, verbose=True)
        task_completion = chat(query="杭州今天天气怎么样？")
        print(task_completion)
        print(chat.task_completions)
