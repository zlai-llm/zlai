import chardet
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Iterable, Optional, Callable, get_args
from langchain.prompts import PromptTemplate

try:
    from langchain_experimental.tools import PythonAstREPLTool
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_experimental")

from ..utils import LoggerMixin, pkg_config
from ..prompt import MessagesPrompt
from ..llms import TypeLLM, TypeLocalGenerate, TypeZhipuGenerate, TypeAliGenerate
from ..embedding import TypeEmbedding
from ..schema import Message, UserMessage, SystemMessage
from ..parse import ParseCode
from .config import *
from .prompt.tasks import TaskDescription, TaskCompletion, FreezeTaskCompletion


__all__ = [
    "AgentMixin",
    "AgentScriptMixin",
    "AgentObservationMixin",
    "AgentParseDataMixin",
    "ShowMessages",
    "StreamMessage",
]


@dataclass
class StreamMessage:
    not_find_content: Optional[str] = "**未在知识库中找到相关信息**...\n\n"
    not_find_table: Optional[str] = "**未在数据库中找到相关表，请您提供更为准确的表名，我再为您解答**...\n\n"
    thinking: Optional[str] = "**正在思考**...\n\n"
    write_script: Optional[str] = "**正在编写相关程序**...\n\n"
    run_script: Optional[str] = "**执行程序**...\n\n"
    script_result: Optional[str] = "**执行结果**:\n\n"
    observation_answer: Optional[str] = "**总结回答**:\n\n"


class ShowMessages(BaseModel):
    """"""
    messages: List[Message] = Field(default=[], description="")
    drop_system: Optional[bool] = Field(default=True, description="")
    content_length: Optional[int] = Field(default=None, description="")
    few_shot: Optional[bool] = Field(default=True, description="")
    logger_name: Optional[str] = Field(default="Logger", description="")


class AgentMixin(LoggerMixin):
    """"""
    agent_name: Optional[str] = None

    llm: Optional[TypeLLM]
    embedding: Optional[TypeEmbedding]
    stream: Optional[bool]
    incremental: Optional[bool]

    system_message: Optional[SystemMessage] = None
    system_template: Optional[PromptTemplate] = None
    prompt_template: Optional[PromptTemplate] = None
    few_shot: Optional[List[Message]] = None
    messages_prompt: Optional[MessagesPrompt] = None

    # memory
    use_memory: Optional[bool]
    max_memory_messages: Optional[int]
    task_completions: Optional[List[TaskCompletion]]

    stream: Optional[bool]
    stream_message: Optional[StreamMessage] = StreamMessage()
    show_messages: Optional[ShowMessages] = StreamMessage()

    def __call__(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Union[TaskCompletion, Iterable[TaskCompletion]]:
        """"""
        if self.stream or kwargs.get("stream", None):
            return self.stream_generate(query=query, *args, **kwargs)
        else:
            return self.generate(query=query, *args, **kwargs)

    def _clear_prompt(self):
        """"""
        self.system_message = None
        self.system_template = None
        self.prompt_template = None
        self.few_shot = None
        self.messages_prompt = None

    def _make_system_message(self, **kwargs: Any) -> SystemMessage:
        """"""
        if self.system_message:
            return self.system_message
        elif self.system_template:
            self.system_message = SystemMessage(content=self.system_template.format_prompt(**kwargs).to_string())
            return self.system_message

    def _show_messages(
            self,
            messages: List[Message],
            drop_system: Optional[bool] = True,
            content_length: Optional[int] = None,
            few_shot: Optional[bool] = True,
            logger_name: Optional[str] = "Logger",
    ) -> None:
        """"""
        self._logger_messages_start(name=logger_name)

        show_messages = messages
        if drop_system:
            show_messages = [message for message in messages if message.role != 'system']
        if not few_shot:
            show_messages = messages[-1:]

        for message in show_messages:
            if content_length:
                show_content = message.content[:content_length]
            else:
                if len(message.content) <= 100:
                    show_content = message.content
                else:
                    show_content = message.content[:100] + '...'
            self._logger_messages(role=f"{message.role} [{len(message.content)}]", content=show_content)
        self._logger_messages_end(name=logger_name)

    def _make_memory_messages(self, task_completion: TaskCompletion) -> List[Message]:
        """"""
        memory_messages = []
        if hasattr(self, "max_memory_messages") and self.use_memory and self.max_memory_messages is not None:
            memory_messages = task_completion.memory_messages[- (self.max_memory_messages * 2):]
            task_completion.memory_messages.append(UserMessage(content=task_completion.query))
        return memory_messages

    def _make_messages(
            self,
            content: Optional[str] = None,
            task_completion: Optional[TaskCompletion] = None,
            **kwargs: Any
    ) -> List[Message]:
        """
        1. merge system message and few-shot
        2. merge memory message
        """
        # messages prompt
        if self.messages_prompt:
            messages = self.messages_prompt.prompt_format(content=content, **kwargs)

        # few-shot
        else:
            messages = []
            if self.system_template:
                system_content = self.system_template.format_prompt(**kwargs).to_string()
                self.system_message = SystemMessage(content=system_content)

            if self.system_message:
                messages.append(self.system_message)
            if self.few_shot:
                messages.extend(self.few_shot)
            if self.prompt_template:
                content = self.prompt_template.format_prompt(content=content, **kwargs).to_string()
            messages.append(UserMessage(content=content))

        # memory messages
        memory_messages = self._make_memory_messages(task_completion=task_completion)
        return memory_messages + messages

    def make_messages_and_invoke(self, task_completion, **kwargs) -> TaskCompletion:
        """"""
        messages = self._make_messages(content=kwargs.get("content"), **kwargs)
        self._show_messages(
            messages=messages,
            drop_system=kwargs.get("drop_system", True),
            content_length=kwargs.get("content_length", None),
            few_shot=kwargs.get("few_shot", True),
            logger_name=kwargs.get("logger_name", "Logger"),
        )
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        return task_completion

    def _load_url_content(
            self,
            url: str,
            features: Optional[str] = "html.parser",
            is_soup: Optional[bool] = False,
            timeout: Optional[int] = 10,
    ) -> Union[str, BeautifulSoup, None]:
        """"""
        try:
            self._logger(msg=f"[{self.agent_name}] Loading URL: {url} \n", color="blue")
            page_content = requests.get(url, headers=config.headers, timeout=timeout)
            encoding = chardet.detect(page_content.content)["encoding"]
            soup = BeautifulSoup(page_content.content, features=features, from_encoding=encoding)
            page_text = soup.get_text()
            self._logger(msg=f"[{self.agent_name}] Loading SUCCESS. \n", color="blue")
            if is_soup:
                return soup
            else:
                return page_text
        except Exception as e:
            error_msg = f"Error fetching page content: {e}"
            self._logger(msg=f"[AgentMixin] Failed load url: {url}; \nError: {error_msg}", color="red")

    def _get_task_mapping(self, task_list: List[TaskDescription]) -> Dict:
        """"""
        task_mapping = dict()
        for task in task_list:
            task_mapping.update({task.task_name: task.task_id})
        return task_mapping

    def _deep_copy_task_completion(
            self,
            task_completion: TaskCompletion,
            drop_delta: bool = False,
    ) -> TaskCompletion:
        """"""
        freeze_task_completion = FreezeTaskCompletion.model_validate(task_completion.model_dump())
        new_task_completions = TaskCompletion.model_validate(freeze_task_completion.model_dump())
        new_task_completions.task_description = task_completion.task_description

        if drop_delta:
            new_task_completions.delta = ""
        return new_task_completions

    def _make_task_completion(self, query: Union[str, TaskCompletion], **kwargs) -> TaskCompletion:
        """"""
        if isinstance(query, TaskCompletion):
            task_completion = self._deep_copy_task_completion(query)
            task_completion = task_completion.model_copy(update=kwargs)
        elif hasattr(self, "task_completions") and isinstance(query, str) and len(self.task_completions) > 0:
            task_completion = self._deep_copy_task_completion(self.task_completions[-1])
            task_completion = task_completion.model_copy(update=kwargs)
            task_completion.query = query
        else:
            task_completion = TaskCompletion.model_validate(kwargs)
            task_completion.query = query
        return task_completion

    def _new_stream_line(
            self,
            task_completion: TaskCompletion,
            n: Optional[int] = 1
    ) -> TaskCompletion:
        """"""
        task_completion = self._deep_copy_task_completion(task_completion)
        task_completion.delta = "\n" * n
        return task_completion

    def _add_task_completion_observation(
            self,
            task_completion: TaskCompletion,
            observation: str,
    ) -> TaskCompletion:
        """"""
        task_completion = self._deep_copy_task_completion(task_completion=task_completion)
        task_completion.observation = observation
        task_completion.delta += f"\n```\n{observation}\n```\n\n"
        return task_completion

    def task_info(self, task_list: List[TaskDescription]) -> str:
        """"""
        task_info = "\n".join([f"task_id: {task.task_id}, task_name: {task.task_name}, task_description: {task.task_description}" for task in task_list])
        return task_info

    def get_content_from_stream_response(self, completion: Any, generate_config: Any) -> str:
        """"""
        if pkg_config.python_version >= (3, 10):
            if isinstance(generate_config, TypeZhipuGenerate):
                return completion.choices[0].delta.content
            else:
                return completion.choices[0].message.content
        elif (3, 8) <= pkg_config.python_version < (3, 10):
            for type_gen in get_args(TypeZhipuGenerate):
                if isinstance(generate_config, type_gen):
                    return completion.choices[0].delta.content
            return completion.choices[0].message.content
        else:
            raise Exception("Unsupported Python version.")

    def _validate_llm_stream(self, llm: [TypeLLM]):
        """"""
        llm.generate_config.stream = self.stream

    def _trans_generate_stream(self, llm: [TypeLLM], stream: bool):
        llm.generate_config.stream = stream

    def stream_output(self, task_completion: TaskCompletion, message: str) -> TaskCompletion:
        """"""
        task_completion = self._deep_copy_task_completion(task_completion=task_completion)
        task_completion.delta = message
        return task_completion

    def stream_task_message(
            self,
            msg: str,
            task_completion: TaskCompletion,
    ) -> TaskCompletion:
        """"""
        task_completion.content = msg
        task_completion.stream = msg
        task_completion.delta = msg
        return task_completion

    def stream_task_completion(
            self,
            messages: List[Message],
            task_completion: TaskCompletion,
            llm: Optional[TypeLLM] = None
    ) -> Iterable[TaskCompletion]:
        """"""
        stream_content = ""
        if llm is None:
            llm = self.llm
        self._validate_llm_stream(llm=llm)
        completions = llm.generate(messages=messages)
        for completion in completions:
            assistant_content = self.get_content_from_stream_response(
                completion=completion, generate_config=self.llm.generate_config)
            stream_content += assistant_content
            task_completion.content = stream_content
            task_completion.stream = stream_content
            task_completion.delta = assistant_content
            yield task_completion

    def base_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        # start task
        self._logger_agent_start(name=self.agent_name)
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)

        # message
        messages = self._make_messages(content=task_completion.query, **kwargs)
        self._show_messages(messages=messages, few_shot=False, drop_system=True, logger_name=self.agent_name)

        # generate
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Assistant: {task_completion.content}", color="green")
        return task_completion

    def observation_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        messages = self._make_messages(question=query.query, script=query.script, observation=query.observation,)
        self._show_messages(messages=messages, logger_name=self.agent_name, content_length=None)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        self._logger_agent_end(name=self.agent_name)
        return task_completion

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        return TaskCompletion()

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        yield TaskCompletion()


class AgentScriptMixin(AgentMixin):
    """"""
    tool: Optional[PythonAstREPLTool]

    def _trans_invoke_data_str(self, data: Union[pd.DataFrame, pd.Series, str]) -> str:
        """"""
        if isinstance(data, (pd.DataFrame, pd.Series)):
            return data.to_markdown()
        else:
            return str(data)

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)

        self._logger(msg=f"[{self.agent_name}] Start ...\n", color="green")
        self._logger(msg=f"[{self.agent_name}] Question: {task_completion.query}\n", color="green")
        messages = self._make_messages(content=task_completion.query, df_head_markdown=self.df.head().to_markdown())
        self._show_messages(messages=messages, drop_system=True, content_length=None, logger_name=self.agent_name)

        completion = self.llm.generate(messages=messages)
        messages.append(completion.choices[0].message)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Assistant: {task_completion.content}\n", color="green")

        scripts = ParseCode.sparse_script(string=task_completion.content, script="python")
        if len(scripts) == 0:
            self._logger(msg=f"[{self.agent_name}] Not Find Script End.\n", color="green")
            return task_completion
        else:
            task_completion.script = scripts[0]
            self._logger(msg=f"[{self.agent_name}] Script: ```\n{task_completion.script}\n```", color="magenta")
            invoke_data = self.tool.invoke(input=task_completion.script)
            task_completion.observation = self._trans_invoke_data_str(data=invoke_data)
            self._logger(msg=f"[{self.agent_name}] Tools invoke: {task_completion.observation}\n", color="green")
        return task_completion


class AgentObservationMixin(AgentMixin):
    """"""

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)

        messages = self._make_messages(question=query.query, script=query.script, observation=query.observation, )
        self._show_messages(messages=messages, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer: {task_completion.content}", color="yellow")
        self._logger(msg=f"[{self.agent_name}] End ...\n", color="green")
        return task_completion


class AgentParseDataMixin(AgentMixin):
    """"""

