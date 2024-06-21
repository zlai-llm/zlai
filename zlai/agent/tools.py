from typing import Any, List, Dict, Union, Tuple, Iterable, Optional, Callable

from ..llms import TypeLLM
from ..schema import Message, SystemMessage, AssistantMessage, ToolsMessage
from ..prompt import MessagesPrompt
from .base import AgentMixin
from .prompt.tasks import TaskCompletion
from .prompt.chat import *
from .agent import dispatch_tool

__all__ = [
    "ToolsAgent",
]


class ToolsAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            incremental: Optional[bool] = True,
            agent_name: Optional[str] = "Tools Agent",
            system_message: Optional[SystemMessage] = PromptChat.system_message,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            hooks: Optional[Dict[str, Callable]] = None,
            use_memory: Optional[bool] = False,
            max_memory_messages: Optional[int] = None,
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
        self.hooks = hooks
        self.use_memory = use_memory
        self.max_memory_messages = max_memory_messages
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def _agent_start_action(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Tuple[TaskCompletion, List[Message]]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        messages = self._make_messages(content=task_completion.query, task_completion=task_completion)
        self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name)
        task_completion.memory_messages = messages
        return task_completion, messages

    def _call_tools(
            self,
            task_completion: TaskCompletion,
            message: Message,
            tool_name: Optional[str] = None,
            tool_params: Optional[Dict] = None,
            hooks: Optional[Dict] = None,
    ):
        """"""
        self._logger(msg=f"[{self.agent_name}] Answer: {message.content}", color="red")
        self._logger(msg=f"[{self.agent_name}] Call Tool: {tool_name}", color="magenta")
        self._logger(msg=f"[{self.agent_name}] Tool Params: {tool_params}", color="magenta")
        data = dispatch_tool(tool_name=tool_name, tool_params=tool_params, hooks=hooks)
        self._logger(msg=f"[{self.agent_name}] Tool Data: {data}", color="magenta")
        task_completion.memory_messages.append(
            ToolsMessage(content=str(data), tool_call_id=message.tool_calls[0].id))

    def _agent_end_action(self, task_completion):
        """"""
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        task_completion.memory_messages.append(AssistantMessage(content=task_completion.content))

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion, messages = self._agent_start_action(query, *args, **kwargs)
        completion = self.llm.generate(messages=messages)
        task_completion.memory_messages.append(completion.choices[0].message)
        self._call_tools(
            task_completion=task_completion, message=completion.choices[0].message,
            tool_name=completion.choices[0].message.tool_calls[0].function.name,
            tool_params=eval(completion.choices[0].message.tool_calls[0].function.arguments),
            hooks=self.hooks
        )
        completion = self.llm.generate(messages=task_completion.memory_messages)
        task_completion.content = completion.choices[0].message.content
        self._agent_end_action(task_completion=task_completion)
        return task_completion
