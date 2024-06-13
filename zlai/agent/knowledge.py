from typing import Any, Union, Callable, Iterable, Optional
from dataclasses import dataclass

from ..llms import TypeLLM
from ..embedding import Embedding
from ..schema import Message, SystemMessage, UserMessage, AssistantMessage
from ..elasticsearch import *
from .base import AgentMixin
from .tasks import TaskSwitch
from .chat import ChatAgent
from .prompt.tasks import TaskCompletion, TaskDescription, TaskParameters
from .prompt.knowledge import *


__all__ = [
    "Knowledge",
    "KnowledgeAgent",
]


@dataclass
class ErrorMessage:
    """"""
    not_find_content: Optional[str] = "未在知识库中找到相关信息..."


class KnowledgeAgent(AgentMixin):
    """"""
    index_name: Optional[str]
    elasticsearch_host: Optional[str]
    elasticsearch_tool: Optional[ElasticSearchTools]

    def __init__(
            self,
            agent_name: Optional[str] = "Knowledge Agent",
            llm: Optional[TypeLLM] = None,
            embedding: Optional[Embedding] = None,
            system_message: Optional[SystemMessage] = PromptKnowledge.system_message,
            prompt_template: Optional[PromptTemplate] = PromptKnowledge.summary_prompt,
            index_name: Optional[str] = None,
            elasticsearch_host: Optional[str] = None,
            stream: Optional[bool] = False,
            error_message: Optional[ErrorMessage] = ErrorMessage(),
            use_memory: Optional[bool] = False,
            max_memory_messages: Optional[int] = None,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any
    ):
        """"""
        self.agent_name = agent_name
        self.llm = llm
        self.embedding = embedding
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.index_name = index_name
        self.elasticsearch_host = elasticsearch_host
        self.stream = stream
        self.error_message = error_message
        self.use_memory = use_memory
        self.max_memory_messages = max_memory_messages
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs
        self.set_elasticsearch()
        self._validate()

    def _validate(self):
        """"""
        if self.max_memory_messages:
            if not 0 < self.max_memory_messages < 20:
                raise ValueError("max_memory_messages must be between 1 and 20.")

    def set_elasticsearch(self):
        """"""
        con = get_es_con(hosts=self.elasticsearch_host)
        self.elasticsearch_tool = ElasticSearchTools(index_name=self.index_name, con=con)

    def search_content(
            self,
            question: Optional[str] = None,
            thresh: Optional[float] = 0.8
    ) -> Union[str, None]:
        """"""
        question_vector = self.embedding.embedding(text=tuple([question]))
        self.elasticsearch_tool.cos_smi(vector=question_vector.to_list()[0])
        data = self.elasticsearch_tool.execute(1)[0]
        score = data.get("_score")
        title = data.get("_source").get("title")
        content = data.get("_source").get("content")
        self._logger(msg=f"[{self.agent_name}] Find Knowledge Title: {title}, Score: {score:.4f}.", color="green")
        if score < thresh:
            self._logger(msg=f"[{self.agent_name}] Not enough score: {score:.4f}.", color="red")
            return None
        else:
            return content

    def _agent_start_action(self, query, *args, **kwargs):
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        task_completion.observation = self.search_content(question=task_completion.query, thresh=kwargs.get("thresh", 0.8))
        return task_completion

    def _agent_end_action(self, task_completion: TaskCompletion):
        """"""
        task_completion.memory_messages.append(AssistantMessage(content=task_completion.content))
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        self._logger_agent_end(name=self.agent_name)

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._agent_start_action(query=query, *args, **kwargs)
        if task_completion.observation is None:
            task_completion.content = self.error_message.not_find_content
        else:
            messages = self._make_messages(
                content=task_completion.observation, task_completion=task_completion,
                question=task_completion.query, )
            self._show_messages(messages=messages, logger_name=self.agent_name)
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
        task_completion = self._agent_start_action(query=query, *args, **kwargs)
        if task_completion.observation is None:
            task_completion.content = self.error_message.not_find_content
            task_completion.delta = self.error_message.not_find_content
            yield task_completion
        else:
            messages = self._make_messages(
                content=task_completion.observation, task_completion=task_completion,
                question=task_completion.query, )
            self._show_messages(messages=messages, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
        self._agent_end_action(task_completion=task_completion)


class Knowledge(TaskSwitch):
    """"""
    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(
                task=KnowledgeAgent, task_id=0, task_name="信息检索机器人",
                task_description="""可以从文本数据库中查询准确的信息，并以准确信息进行回答。""",
                task_parameters=TaskParameters(
                    verbose=True, use_memory=True, max_memory_messages=10,
                )
            ),
            TaskDescription(
                task=ChatAgent, task_id=1, task_name="聊天机器人",
                task_description="""提供普通对话聊天，不涉及专业知识与即时讯息。""",
                task_parameters=TaskParameters(
                    verbose=True, use_memory=True, max_memory_messages=10,
                )
            ),
        ]
