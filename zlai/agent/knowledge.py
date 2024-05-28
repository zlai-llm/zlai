from typing import Any, Union, Callable, Iterable, Optional
from dataclasses import dataclass

from ..llms import TypeLLM
from ..embedding import Embedding
from ..schema import SystemMessage
from ..elasticsearch import *
from .base import AgentMixin
from .prompt.tasks import TaskDescription, TaskParameters, TaskCompletion
from .prompt.knowledge import *


__all__ = [
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
        self.logger = logger
        self.verbose = verbose
        self.args = args
        self.kwargs = kwargs
        self.set_elasticsearch()

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

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        task_completion.observation = self.search_content(question=task_completion.query, thresh=kwargs.get("thresh", 0.8))
        if task_completion.observation is None:
            task_completion.content = self.error_message.not_find_content
        else:
            messages = self._make_messages(question=task_completion.query, content=task_completion.observation,)
            self._show_messages(messages=messages, logger_name=self.agent_name)
            completion = self.llm.generate(messages=messages)
            task_completion.content = completion.choices[0].message.content
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        self._logger_agent_end(name=self.agent_name)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        task_completion.observation = self.search_content(question=task_completion.query, thresh=kwargs.get("thresh", 0.8))
        if task_completion.observation is None:
            task_completion.content = self.error_message.not_find_content
            task_completion.delta = self.error_message.not_find_content
            yield task_completion
        else:
            messages = self._make_messages(question=task_completion.query, content=task_completion.observation,)
            self._show_messages(messages=messages, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        self._logger_agent_end(name=self.agent_name)
