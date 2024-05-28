from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from typing import List, ClassVar
from ...schema.messages import Message, SystemMessage, UserMessage, AssistantMessage


__all__ = [
    "PromptTemplate",
    "PromptWeather",
    "weather_task_plan",
]


system_message = SystemMessage(content="You are a helpful Weather Announcer.")

PromptWeather = """请根据以下天气信息回答问题。

信息：\n```\n{weather}\n```
问题：{question}"""

prompt_weather = PromptTemplate(
    input_variables=["weather", "question"],
    template=PromptWeather)


@dataclass
class PromptWeather:
    """"""
    # weather
    system_message: SystemMessage = system_message
    prompt_weather: PromptTemplate = prompt_weather


weather_task_plan = [
    UserMessage(content="余杭区的天气怎么样？"),
    AssistantMessage(content=str([{"task_id": 1,}])),
]
