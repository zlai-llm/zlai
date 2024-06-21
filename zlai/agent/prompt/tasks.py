from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from typing import Any, List, Dict, Union, Type, Optional, Callable, ClassVar
from dataclasses import dataclass, field, fields

from ...llms import TypeLLM
from ...embedding import TypeEmbedding
from ...prompt import MessagesPrompt
from ...schema.messages import Message, UserMessage, AssistantMessage, SystemMessage


__all__ = [
    "TaskParameters",
    "TaskDescription",
    "TaskSwitchPrompt",
    "TaskPlanPrompt",
    "TaskAnswer",
    "TaskCompletion",
    "FreezeTaskCompletion",
    "TaskPlanCompletion",
]


@dataclass
class TaskParameters:
    """"""
    # model
    llm: Optional[TypeLLM] = field(default=None)
    embedding: Optional[TypeEmbedding] = field(default=None)

    # database
    db: Optional[Any] = field(default=None)
    db_path: Optional[str] = field(default=None)

    # messages
    system_message: Optional[SystemMessage] = field(default=None)
    system_template: Optional[PromptTemplate] = field(default=None)
    prompt_template: Optional[PromptTemplate] = field(default=None)
    few_shot: Optional[List[Message]] = field(default=None)
    messages_prompt: Optional[MessagesPrompt] = field(default=None)
    use_memory: Optional[bool] = field(default=False)
    max_memory_messages: Optional[int] = field(default=None)

    # logger
    logger: Optional[Callable] = field(default=None)
    verbose: Optional[bool] = field(default=None)

    # ElasticSearch
    index_name: Optional[str] = field(default=None)
    elasticsearch_host: Optional[str] = field(default=None)

    kwargs: Optional[Dict] = field(default=None)

    def params(self) -> Dict[str, any]:
        _params = {field.name: getattr(self, field.name) for field in fields(self) if getattr(self, field.name) is not None}
        if self.kwargs is not None:
            _params.update(self.kwargs)
        return _params


class TaskDescription(BaseModel):
    """"""
    class Config:
        arbitrary_types_allowed = True

    task: Optional[Callable] = Field(default=None, description="")
    task_id: Optional[int] = Field(default=None, description="")
    task_name: Optional[str] = Field(default=None, description="")
    task_description: Optional[str] = Field(default=None, description="")
    task_parameters: Optional[TaskParameters] = Field(default=TaskParameters(), description="")


class TaskAnswer(BaseModel):
    task_id: Optional[int] = Field(default=None, description="")
    task_name: Optional[str] = Field(default=None, description="")
    task_query: Optional[Any] = Field(default=None, description="")
    task_answer: Optional[Any] = Field(default=None, description="")


PromptTask: str = """Given a user question, determine the user's question is suitable for which task below: 

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


@dataclass
class TaskSwitchPrompt:
    """"""
    task_prompt: PromptTemplate = PromptTemplate(input_variables=["task_info"], template=PromptTask)


@dataclass
class TaskPlanPrompt:
    task_prompt_plan: PromptTemplate = PromptTemplate(input_variables=["task_info"], template=PromptTask)
    few_shot_task_id_lst: ClassVar[List[Message]] = few_shot_task_id_lst
    messages_prompt: MessagesPrompt = messages_prompt


class FreezeTaskCompletion(BaseModel):
    """"""
    query: Optional[str] = Field(default=None, description="")
    task_id: Optional[int] = Field(default=None, description="")
    task_name: Optional[str] = Field(default=None, description="")
    content: Optional[str] = Field(default=None, description="")
    stream: Optional[str] = Field(default=None, description="")
    delta: Optional[str] = Field(default=None, description="")
    script: Optional[str] = Field(default=None, description="")
    parsed_data: Optional[Any] = Field(default=None, description="")
    observation: Optional[str] = Field(default=None, description="")
    data: Optional[Dict[str, List]] = Field(default=None, description="")
    query_id: Optional[int] = Field(default=None, description="")
    origin_query: Optional[str] = Field(default=None, description="")
    total_question: Optional[List[str]] = Field(default=None, description="")
    next_question: Optional[str] = Field(default=None, description="")
    previous_question: Optional[str] = Field(default=None, description="")
    memory_messages: Optional[List[Union[Message, UserMessage, AssistantMessage]]] = Field(default=[], description="历史消息")


class TaskCompletion(FreezeTaskCompletion):
    """"""
    task_description: Optional[TaskDescription] = Field(default=None, description="")


class TaskPlanCompletion(BaseModel):
    """"""
    task: Optional[str] = Field(default=None, description="任务/问题描述")
    task_completion: Optional[TaskCompletion] = Field(default=None, description="任务/问题回答")
