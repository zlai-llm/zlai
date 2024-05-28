from pydantic import BaseModel, Field
from typing import Any, Union, Optional, Callable

from ..llms import TypeLLM
from ..prompt import MessagesPrompt
from ..parse import ParseDict
from .base import AgentMixin
from .prompt.address import *
from .prompt.tasks import TaskCompletion


__all__ = [
    "StandardAddress",
    "AddressAgent",
]


class StandardAddress(BaseModel):
    """"""
    province: Optional[str] = Field(default=None, description="省")
    city: Optional[str] = Field(default=None, description="市")
    district: Optional[str] = Field(default=None, description="区")


class AddressAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            agent_name: Optional[str] = "Address Agent",
            messages_prompt: Optional[MessagesPrompt] = PromptAddress.messages_prompt,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.agent_name = agent_name
        self.messages_prompt = messages_prompt
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs

    def __call__(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        return self.generate(query=query, *args, **kwargs)

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger(msg=f"[{self.agent_name}] User Question: {task_completion.query}", color='green')
        messages = self._make_messages(content=task_completion.query)
        self._show_messages(messages=messages, few_shot=False, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer:\n{task_completion.content}", color="green")
        parsed_address = ParseDict.eval_dict(string=task_completion.content)
        self._logger(msg=f"[{self.agent_name}] Parsed address:\n{parsed_address}", color="yellow")
        if len(parsed_address) == 0:
            task_completion.parsed_data = StandardAddress()
        else:
            task_completion.parsed_data = StandardAddress.model_validate(parsed_address[0])
        return task_completion
