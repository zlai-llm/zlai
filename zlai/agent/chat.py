from typing import Any, List, Union, Iterable, Optional, Callable

from ..llms import TypeLLM
from ..schema import Message, SystemMessage
from ..prompt import MessagesPrompt
from .base import AgentMixin
from .prompt.tasks import TaskDescription, TaskParameters, TaskCompletion
from .prompt.chat import *


__all__ = [
    "ChatAgent",
]


class ChatAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            incremental: Optional[bool] = True,
            agent_name: Optional[str] = "Chat Agent",
            system_message: Optional[SystemMessage] = PromptChat.system_message,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.stream = stream
        self.incremental = incremental
        self.agent_name = agent_name
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        messages = self._make_messages(content=task_completion.query)
        self._show_messages(messages=messages, drop_system=True, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        messages = self._make_messages(content=task_completion.query)
        self._show_messages(messages=messages, drop_system=True, few_shot=False, logger_name=self.agent_name)
        stream_task_instance = self.stream_task_completion(
            llm=self.llm, messages=messages, task_completion=task_completion)
        for task_completion in stream_task_instance:
            yield task_completion
        yield self._new_stream_line(task_completion=task_completion)
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)


task_chat = TaskDescription(
    task=ChatAgent, task_name="聊天机器人",
    task_description="""提供普通对话聊天，不涉及专业知识与即时讯息。""",
)
