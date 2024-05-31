from typing import Any, List, Literal, Optional, Callable
from langchain.prompts import PromptTemplate
import pandas as pd

try:
    from langchain_experimental.tools import PythonAstREPLTool
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_experimental")

from ..prompt import MessagesPrompt
from ..schema import Message, UserMessage, AssistantMessage, SystemMessage
from ..embedding import Embedding
from ..llms import *
from ..parse import ParseCode
from .base import *
from .prompt.csv import *
from .prompt.tasks import TaskCompletion, TaskDescription
from .tasks import TaskSequence, TaskSwitch


__all__ = [
    "CSV",
    "CSVAgent",
    "CSVQA",
    "CSVScript",
    "CSVObservation",
    "CSVScriptWithObservation",
]


class CSVAgent(AgentMixin):
    """"""
    agent_name: Optional[str] = "CSV-Agent"
    csv_path: Optional[str]
    llm: Optional[TypeLLM]
    embedding: Optional[Embedding]
    system_message: Optional[SystemMessage]
    system_template: Optional[PromptTemplate]
    prompt_template: Optional[PromptTemplate]
    few_shot: Optional[List[Message]]
    messages_prompt: Optional[MessagesPrompt]
    df: Optional[pd.DataFrame]
    tool: Optional[PythonAstREPLTool]
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            csv_path: Optional[str] = None,
            agent_name: Optional[str] = "CSV-Agent",
            llm: Optional[TypeLLM] = None,
            embedding: Optional[Embedding] = None,
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = PromptDataFrame.prompt_dataframe_code,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,

            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            **kwargs,
    ):
        self.csv_path = csv_path
        self.agent_name = agent_name
        self.llm = llm
        self.embedding = embedding
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt

        self.logger = logger
        self.verbose = verbose

        self.stream = stream

    def __call__(self, query, *args, **kwargs):
        """"""
        answer = self.generate(query=query)
        return answer

    def init_csv(self):
        """"""
        if self.csv_path:
            self.df = pd.read_csv(self.csv_path)
            self._make_system_message(df_head_markdown=self.df.head().to_markdown())
            self.tool = PythonAstREPLTool(locals={"df": self.df})
        else:
            raise ValueError(f"CSVAgent path not found: {self.csv_path}")

    def _trans_invoke_data_str(self, data: Union[pd.DataFrame, pd.Series, str]) -> str:
        """"""
        if isinstance(data, (pd.DataFrame, pd.Series)):
            return data.to_markdown()
        else:
            return str(data)


class CSVQA(AgentObservationMixin, CSVAgent):
    """"""

    def __init__(
            self,
            csv_path: Optional[str] = None,
            agent_name: Optional[str] = "CSVAgent-QA",
            system_template: Optional[PromptTemplate] = PromptDataFrame.prompt_csv,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.csv_path = csv_path
        self.system_template = system_template
        self.agent_name = agent_name
        self.init_csv()

    def generate(
            self,
            query: Union[str, TaskCompletion] = None,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger(msg=f"[{self.agent_name}] Start ...\n", color="green")
        self._logger(msg=f"[{self.agent_name}] Question: {query}\n", color="green")

        messages = self._make_messages(content=task_completion.query, df_head_markdown=self.df.head().to_markdown())
        self._show_messages(messages=messages, content_length=None, drop_system=True, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer: {task_completion.content}", color="yellow")
        return task_completion


class CSVScript(CSVAgent):
    """"""
    agent_name: Optional[str] = "CSVAgent-Script"
    csv_path: Optional[str]

    def __init__(
            self,
            agent_name: Optional[str] = "CSVAgent-Script",
            csv_path: Optional[str] = None,
            system_template: Optional[PromptTemplate] = PromptDataFrame.prompt_dataframe_code,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.agent_name = agent_name
        self.csv_path = csv_path
        self.system_template = system_template
        self.init_csv()

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
        else:
            task_completion.script = scripts[0]
            self._logger(msg=f"[{self.agent_name}] Script: ```\n{task_completion.script}\n```", color="magenta")
            invoke_data = self.tool.invoke(input=task_completion.script)
            task_completion.observation = self._trans_invoke_data_str(data=invoke_data)
            self._logger(msg=f"[{self.agent_name}] Tools invoke: {task_completion.observation}\n", color="green")
        return task_completion


class CSVObservation(CSVAgent):
    """"""
    agent_name: Optional[str] = "CSVAgent-Observation"
    csv_path: Optional[str]

    def __init__(
            self,
            agent_name: Optional[str] = "CSVAgent-Observation",
            csv_path: Optional[str] = None,
            system_message: Optional[SystemMessage] = PromptDataFrame.system_message_dataframe_summary,
            prompt_template: Optional[PromptTemplate] = PromptDataFrame.prompt_dataframe_observation_summary,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.agent_name = agent_name
        self.csv_path = csv_path
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.init_csv()

    def __call__(
            self,
            query: TaskCompletion,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        return self.generate(query=query, *args, **kwargs)

    def generate(
            self,
            query: TaskCompletion,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)

        messages = self._make_messages(question=query.query, script=query.script, observation=query.observation,)
        self._show_messages(messages=messages, drop_system=False, content_length=None, logger_name=self.agent_name)
        completion = self.llm.generate(messages=messages)
        task_completion.content = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Final Answer: {task_completion.content}", color="yellow")
        self._logger(msg=f"[{self.agent_name}] End ...\n", color="green")
        return task_completion


class CSVScriptWithObservation(TaskSequence):
    """"""
    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(task=CSVScript, task_id=0, task_name="DataFrame脚本", ),
            TaskDescription(task=CSVObservation, task_id=1, task_name="数据总结", ),
        ]


class CSV(TaskSwitch):
    """"""
    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(
                task=CSVScriptWithObservation, task_id=0, task_name="数据提取与计算机器人",
                task_description="""可以帮你写一段`DataFrame`脚本代码查询表中数据的具体信息""",
            ),
            TaskDescription(
                task=CSVQA, task_id=1, task_name="数据表介绍机器人",
                task_description="""可以介绍并回答数据表的基本信息，但不能够查询真实的数据，只能做一般性的介绍。""",
            ),
        ]
