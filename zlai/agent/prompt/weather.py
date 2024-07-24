from dataclasses import dataclass
from ...prompt import PromptTemplate
from ...schema.messages import SystemMessage, UserMessage, AssistantMessage
from ..schema import AgentPrompt


__all__ = [
    "prompt_weather",
    "weather_task_plan",
]


system_message = SystemMessage(content="You are a helpful Weather Announcer.")

PromptWeather = """请根据以下天气信息回答问题。

信息：\n```\n{weather}\n```
问题：{question}"""

prompt_weather = PromptTemplate(
    input_variables=["weather", "question"],
    template=PromptWeather)

prompt_weather = AgentPrompt(system_message=system_message, prompt_template=prompt_weather)

weather_task_plan = [
    UserMessage(content="余杭区的天气怎么样？"),
    AssistantMessage(content=str([{"task_id": 1,}])),
]
