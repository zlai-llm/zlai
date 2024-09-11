from typing import Any, List, Union, Tuple, Iterable, Optional, Callable

from zlai.llms import TypeLLM
from zlai.types.messages import Message, AssistantMessage
from zlai.types.agent import TaskDescription, TaskCompletion
from zlai.prompt import AgentPrompt
from zlai.prompt.graph import prompt_entities, prompt_relations
from zlai.parse import ParseCode
from zlai.agent.base import AgentMixin
from zlai.agent.tasks import TaskSequence


__all__ = [
    "EntityAgent",
    "RelationAgent",
    "GraphAgent",
]


class EntityAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            agent_name: Optional[str] = "Entity Agent",
            agent_prompt: Optional[AgentPrompt] = prompt_entities,
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
        self.agent_prompt = agent_prompt
        self.use_memory = use_memory
        self.max_memory_messages = max_memory_messages
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs
        self._init_prompt()

    def _agent_start_action(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Tuple[TaskCompletion, List[Message]]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query[:128])
        messages = self._make_messages(content=task_completion.query, task_completion=task_completion, **kwargs)
        self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name, content_length=128)
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
        task_completion.data = {
            "content": task_completion.query,
            "entity_types": kwargs.get("entity_types"),
            "entities": ParseCode.sparse_script(string=task_completion.content)[0],
        }
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
        task_completion.data = {
            "content": task_completion.query,
            "entity_types": kwargs.get("entity_types"),
            "entities": ParseCode.sparse_script(string=task_completion.content)[0],
        }
        yield self._new_stream_line(task_completion=task_completion)
        self._agent_end_action(task_completion=task_completion)


class RelationAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            stream: Optional[bool] = False,
            agent_name: Optional[str] = "Relation Agent",
            agent_prompt: Optional[AgentPrompt] = prompt_relations,
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
        self.agent_prompt = agent_prompt
        self.use_memory = use_memory
        self.max_memory_messages = max_memory_messages
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs
        self._init_prompt()

    def _agent_start_action(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query[:128])
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
        messages = self._make_messages(**task_completion.data)
        self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name, content_length=128)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
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
        messages = self._make_messages(**task_completion.data)
        self._show_messages(messages=messages, drop_system=False, logger_name=self.agent_name, content_length=128)
        stream_task_instance = self.stream_task_completion(
            llm=self.llm, messages=messages, task_completion=task_completion)
        for task_completion in stream_task_instance:
            yield task_completion
        yield self._new_stream_line(task_completion=task_completion)
        self._agent_end_action(task_completion=task_completion)
        return task_completion


class GraphAgent(TaskSequence):
    """"""

    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(task=EntityAgent, task_id=0, task_name="LongWriteAgentPlan", ),
            TaskDescription(task=RelationAgent, task_id=1, task_name="LongWriteAgentWrite", ),
        ]
