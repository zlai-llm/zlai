import unittest
from zlai.schema import *
from zlai.llms import Zhipu, GLM4AirGenerateConfig, GLM4GenerateConfig
from zlai.agent import *


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

    def test_weather(self):
        """"""
        # Step1：定义两个agent，用于执行解析地址，与天气查询
        task_weather = [
            TaskDescription(
                task=AddressAgent,
                task_id=0,
                task_name="地址解析机器人",
                task_description="""可以帮助你解析文本中的地址信息，并返回标准地址字段信息。""",
                task_parameters=TaskParameters(
                    llm=Zhipu(generate_config=GLM4GenerateConfig()),
                    verbose=True,
                )
            ),
            TaskDescription(
                task=WeatherAgent,
                task_id=1,
                task_name="天气播报机器人",
                task_description="""提供具体的地址信息后可以帮助你查询当地的天气情况，必须提供标准地址。""",
                task_parameters=TaskParameters(
                    llm=Zhipu(generate_config=GLM4GenerateConfig()),
                    verbose=True,
                )
            ),
        ]

        # Step2：构建Task Sequence
        task_seq = TaskSequence(task_list=task_weather, verbose=True)

        # Step3：执行任务
        query = "杭州余杭今天天气怎么样？"
        answer = task_seq(query=query)
        print(answer.content)
