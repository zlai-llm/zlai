from typing import Any, List, Dict, Optional, Callable
from pydantic import BaseModel, Field, ConfigDict
from zlai.llms import TypeLLM
from zlai.embedding import TypeEmbedding
from zlai.schema import Message, SystemMessage, TypeMessage
from zlai.prompt import PromptTemplate, MessagesPrompt


__all__ = [
    "TaskParameters",
    "TaskDescription",
    "TaskAnswer",
    "TaskCompletion",
    "FreezeTaskCompletion",
    "TaskPlanCompletion",
]


class TaskParameters(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # model
    llm: Optional[TypeLLM] = Field(default=None)
    embedding: Optional[TypeEmbedding] = Field(default=None)

    # database
    db: Optional[Any] = Field(default=None)
    db_path: Optional[str] = Field(default=None)

    # messages
    system_message: Optional[SystemMessage] = Field(default=None)
    system_template: Optional[PromptTemplate] = Field(default=None)
    prompt_template: Optional[PromptTemplate] = Field(default=None)
    few_shot: Optional[List[Message]] = Field(default=None)
    messages_prompt: Optional[MessagesPrompt] = Field(default=None)
    use_memory: Optional[bool] = Field(default=False)
    max_memory_messages: Optional[int] = Field(default=None)

    # logger
    logger: Optional[Callable] = Field(default=None)
    verbose: Optional[bool] = Field(default=None)

    # ElasticSearch
    index_name: Optional[str] = Field(default=None)
    elasticsearch_host: Optional[str] = Field(default=None)

    # tools
    hooks: Optional[Dict[str, Callable]] = Field(default=None)
    tools_description: Optional[List] = Field(default=None)
    tools_params_fun: Optional[Callable] = Field(default=None)

    kwargs: Optional[Dict] = Field(default=None)

    def params(self) -> Dict[str, any]:
        return self.model_dump()


class TaskDescription(BaseModel):
    """ """
    model_config = ConfigDict(arbitrary_types_allowed=True)
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
    memory_messages: Optional[List[TypeMessage]] = Field(default=[], description="历史消息")


class TaskCompletion(FreezeTaskCompletion):
    """"""
    task_description: Optional[TaskDescription] = Field(default=None, description="")


class TaskPlanCompletion(BaseModel):
    """"""
    task: Optional[str] = Field(default=None, description="任务/问题描述")
    task_completion: Optional[TaskCompletion] = Field(default=None, description="任务/问题回答")
