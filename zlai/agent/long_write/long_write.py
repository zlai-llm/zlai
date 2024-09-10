from typing import Any, List, Union, Tuple, Iterable, Optional, Callable

from zlai.llms import TypeLLM
from zlai.schema import Message, SystemMessage, AssistantMessage
from zlai.prompt import MessagesPrompt, PromptTemplate
from zlai.agent.base import AgentMixin
from zlai.agent.tasks import TaskSequence
from zlai.agent.schema import TaskDescription, TaskCompletion
from zlai.agent.prompt.long_write import *


__all__ = [
    "LongWriteAgent",
    "LongWriteAgentPlan",
    "LongWriteAgentWrite",
]


class LongWriteAgentPlan(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            agent_name: Optional[str] = "Long Write Agent Plan",
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = prompt_long_write_plan.prompt_template,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
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
        self.agent_name = agent_name
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
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
        messages = self._make_messages(instruction=task_completion.query, task_completion=task_completion)
        self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name)
        return task_completion, messages

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
        task_completion.data = {"instruction": task_completion.query}
        self._agent_end_action(task_completion=task_completion)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        task_completion, messages = self._agent_start_action(query, *args, **kwargs)
        stream_task_instance = self.stream_task_completion(
            llm=self.llm, messages=messages, task_completion=task_completion)
        for task_completion in stream_task_instance:
            yield task_completion
        task_completion.data = {"instruction": task_completion.query}
        yield self._new_stream_line(task_completion=task_completion)
        self._agent_end_action(task_completion=task_completion)


class LongWriteAgentWrite(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            agent_name: Optional[str] = "Long Write Agent Write",
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = prompt_long_write.prompt_template,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
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
        self.agent_name = agent_name
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
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
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)
        return task_completion

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
        task_completion = self._agent_start_action(query, *args, **kwargs)
        steps = [line for line in task_completion.content.split("\n\n") if "Paragraph" in line]

        instruction = task_completion.data.get("instruction", "")
        content = f"# {instruction}"
        for step in steps:
            messages = self._make_messages(
                instruction=instruction, step=step, content=content, task_completion=task_completion)
            self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name)
            completion = self.llm.generate(messages=messages)
            step_content = completion.choices[0].message.content
            content += f"\n\n{step_content}"
            self._logger(msg=f"[{self.agent_name}] Step content: {step_content}")

        task_completion.content = content
        self._agent_end_action(task_completion=task_completion)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        task_completion = self._agent_start_action(query, *args, **kwargs)
        steps = [line for line in task_completion.content.split("\n\n") if "Paragraph" in line]

        instruction = task_completion.data.get("instruction", "")
        content = f"# {instruction}"
        for step in steps:
            messages = self._make_messages(
                instruction=instruction, step=step, content=content, task_completion=task_completion)
            self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(
                llm=self.llm, messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
            yield self._new_stream_line(task_completion=task_completion)

            step_content = task_completion.content
            content += f"\n\n{step_content}"
            self._logger(msg=f"[{self.agent_name}] Step content: {step_content}")

        task_completion.content = content
        self._agent_end_action(task_completion=task_completion)
        return task_completion


class LongWriteAgent(TaskSequence):
    """"""

    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(task=LongWriteAgentPlan, task_id=0, task_name="LongWriteAgentPlan", ),
            TaskDescription(task=LongWriteAgentWrite, task_id=1, task_name="LongWriteAgentWrite", ),
        ]
