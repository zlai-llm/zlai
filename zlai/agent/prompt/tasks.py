from ...prompt import MessagesPrompt, PromptTemplate
from ...schema import UserMessage, AssistantMessage, SystemMessage
from ..schema import *


__all__ = [
    "task_switch_prompt",
    "task_plan_prompt",
]


PromptTaskSwitch: str = """Given a user question, determine the user's question is suitable for which task below:

```
{task_info}
```

Return ONLY the TASK ID and nothing else.
"""

system_message_task_plan = SystemMessage(content="""你是一个任务规划机器人，你需要把给定的问题，拆分为一个List，使用问题原文回答。""")

few_shot_task_id_lst = [
    UserMessage(content="""问题: 帮我查询杭州的天气，并从文本数据库中查询“旅游股2024年一季度合计净利润”。\nList: """),
    AssistantMessage(content=str(["查询杭州的天气", "旅游股2024年一季度合计净利润"])),
]

messages_prompt = MessagesPrompt(
    system_message=system_message_task_plan,
    few_shot=few_shot_task_id_lst,
    prompt_template=PromptTemplate(
        input_variables=["content"],
        template="""问题: {content}。\nList: """),
)

task_switch_prompt = AgentPrompt(
    system_template=PromptTemplate(input_variables=["task_info"], template=PromptTaskSwitch))

task_plan_prompt = AgentPrompt(
    prompt_template=PromptTemplate(input_variables=["task_info"], template=PromptTaskSwitch),
    few_shot=few_shot_task_id_lst,
    messages_prompt=messages_prompt,
)
