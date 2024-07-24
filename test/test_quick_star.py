import unittest
from zlai.schema import *
from zlai.llms import Zhipu, GLM4AirGenerateConfig


class TestQuickStar(unittest.TestCase):
    def test_quick_star(self):
        """"""
        messages = [
            SystemMessage(content="你是一个人工智能助手。用于记录我的日常事务。"),
            UserMessage(content="你好，我的好朋友六子昨天早晨吃了2碗粉。"),
            AssistantMessage(content="好的，我记住了。")
        ]

        llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        # 新的问题
        messages.append(UserMessage(content="请问，昨天六子早上吃了几碗粉？"))
        completion = llm.generate(messages=messages)
        print(completion.choices[0].message.content)

    def test_agent(self):
        """"""
        from zlai.agent import ChatAgent, TaskDescription

        task_chat = TaskDescription(
            task=ChatAgent, task_name="聊天机器人",
            task_description="""提供普通对话聊天，不涉及专业知识与即时讯息。""",
        )
        print(task_chat)
