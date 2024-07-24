from pandas import DataFrame
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Tuple, Optional, Callable
from ...llms import TypeLLM
from ...schema import TypeMessage, Message, SystemMessage, AssistantMessage, ToolsMessage
from ...prompt import MessagesPrompt, PromptTemplate
from ..base import AgentMixin
from ..prompt.tasks import TaskCompletion
from ..prompt.chat import prompt_chat
from .register import dispatch_tool, register_tool


__all__ = [
    "Tools",
    "ToolsAgent",
]


class Tools(BaseModel):
    """"""
    tool_descriptions: List[Dict] = Field(default=[], description="Description of the tool")
    tool_hooks: Dict[str, Callable] = Field(default={}, description="Hooks of the tool")
    tool_list: List[Callable] = Field(default=None, description="List of function to be used as tools")
    params_fun: Optional[Callable] = Field(default=None, description="Function to clean the parameters of the tool")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_tools()

    def register_tools(self):
        """"""
        for fun in self.tool_list:
            register_tool(tool_hooks=self.tool_hooks, tool_descriptions=self.tool_descriptions)(fun)

    def dispatch_tool(self, *args: Any, **kwargs: Any) -> Any:
        return dispatch_tool(*args, **kwargs, hooks=self.tool_hooks)


class ToolsAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            incremental: Optional[bool] = True,
            agent_name: Optional[str] = "Tools Agent",
            system_message: Optional[SystemMessage] = prompt_chat.system_message,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            tools: Optional[Tools] = None,
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
        self.tools = tools
        self.use_memory = use_memory
        self.max_memory_messages = max_memory_messages
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs
        self.set_llm_tools()

    def set_llm_tools(self, tool_descriptions: Optional[List] = None):
        """"""
        if tool_descriptions is None:
            if self.tools is None:
                raise ValueError("Tools is not set")
            else:
                self.llm.generate_config.tools = self.tools.tool_descriptions
        else:
            self.llm.generate_config.tools = tool_descriptions

        self._logger(msg=f"[{self.agent_name}] Registered {len(self.tools.tool_hooks)} Tools: {list(self.tools.tool_hooks.keys())}\n", color="green")

    def _clean_tools_params(self, tool_params: Dict) -> Dict:
        """"""
        if self.tools.params_fun:
            tool_params = self.tools.params_fun(tool_params)
            self._logger(msg=f"[{self.agent_name}] Converted Tool Params: {tool_params}", color="magenta")
        return tool_params

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

    def _validate_data(
            self,
            data: Union[str, Dict, List, DataFrame]
    ) -> str:
        """"""
        self._logger(msg=f"[{self.agent_name}] Tool Data Type: {type(data)}, length: {len(data)}", color="magenta")
        if isinstance(data, DataFrame):
            data = data.to_markdown()
        else:
            data = str(data)
        return data

    def _call_tools(
            self,
            task_completion: TaskCompletion,
            message: TypeMessage,
            tool_name: Optional[str] = None,
            tool_params: Optional[Dict] = None,
    ):
        """"""
        self._logger(msg=f"[{self.agent_name}] Answer Content: {message.content}", color="magenta")
        self._logger(msg=f"[{self.agent_name}] Call Tool: {tool_name}", color="magenta")
        self._logger(msg=f"[{self.agent_name}] Tool Params: {tool_params}", color="magenta")
        tool_params = self._clean_tools_params(tool_params)
        data = self.tools.dispatch_tool(tool_name=tool_name, tool_params=tool_params)
        data = self._validate_data(data=data)
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
        task_completion.content = completion.choices[0].message.content
        task_completion.memory_messages.append(completion.choices[0].message)

        if completion.choices[0].finish_reason == "tool_calls":
            self._call_tools(
                task_completion=task_completion, message=completion.choices[0].message,
                tool_name=completion.choices[0].message.tool_calls[0].function.name,
                tool_params=eval(completion.choices[0].message.tool_calls[0].function.arguments),
            )
            completion = self.llm.generate(messages=task_completion.memory_messages)
            task_completion.content = completion.choices[0].message.content
        self._agent_end_action(task_completion=task_completion)
        return task_completion
