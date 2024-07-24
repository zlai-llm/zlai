from typing import Any, List, Dict, Optional, Callable
from dataclasses import field, fields

from ...llms import TypeLLM
from ...embedding import TypeEmbedding
from ...prompt import MessagesPrompt, PromptTemplate
from ...schema import Message, SystemMessage


__all__ = [
    "TaskParameters",
]


# @dataclass
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

    # tools
    hooks: Optional[Dict[str, Callable]] = field(default=None)
    tools_description: Optional[List] = field(default=None)
    tools_params_fun: Optional[Callable] = field(default=None)

    kwargs: Optional[Dict] = field(default=None)

    def params(self) -> Dict[str, any]:
        _params = {field.name: getattr(self, field.name) for field in fields(self) if getattr(self, field.name) is not None}
        if self.kwargs is not None:
            _params.update(self.kwargs)
        return _params
