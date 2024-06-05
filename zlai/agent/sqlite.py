try:
    from langchain_community.utilities.sql_database import SQLDatabase
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install langchain_community")

import sqlite3
import pandas as pd
from typing import Any, List, Union, Tuple, Optional, Callable, Iterable

from ..llms import TypeLLM
from ..embedding import TypeEmbedding
from ..schema import Message, SystemMessage
from ..prompt import MessagesPrompt
from ..parse import ParseCode
from .base import *
from .prompt.sqlite import *
from .prompt.tasks import TaskDescription, TaskParameters, TaskCompletion
from .tasks import TaskSwitch, TaskSequence
from .chat import ChatAgent

# TODO: 在query进入后先提取表名，再进行相似表的匹配。

__all__ = [
    "SQLite",
    "SQLiteAgent",
    "SQLiteTable",
    "SQLiteQA",
    "SQLiteScript",
    "SQLiteObservation",
    "SQLiteScriptWithObservation",
]


class SQLiteAgent(AgentMixin):
    """"""
    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            embedding: Optional[TypeEmbedding] = None,

            agent_name: Optional[str] = "SQLite Agent",
            db: Optional[SQLDatabase] = None,
            db_path: Optional[str] = None,
            catalog_table: Optional[str] = "metadata",

            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,

            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.llm = llm
        self.embedding = embedding
        self.agent_name = agent_name

        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.stream = stream
        self.logger = logger
        self.verbose = verbose

        self.args = args
        self.kwargs = kwargs

        self.db = self.set_database(db=db, db_path=db_path)
        self.catalog = self.set_catalog(
            db_path=db_path, catalog_table=catalog_table
        )

    def set_database(
            self,
            db: Optional[SQLDatabase] = None,
            db_path: Optional[str] = None,
    ) -> SQLDatabase:
        """"""
        if db is None and db_path is None:
            raise ValueError(f"Please specify db or db path.")
        elif db is not None:
            return db
        elif db_path is not None:
            try:
                db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
                self._logger(msg=f"[{self.agent_name}] Connect database success: {db_path}", color="green")
                return db
            except Exception as e:
                raise ValueError(f"Failed to connect to database: {e}")
        else:
            raise ValueError(f"Please specify db or db path.")

    def set_catalog(
            self,
            db_path: Optional[str] = None,
            catalog_table: Optional[str] = None
    ) -> pd.DataFrame:
        """"""
        try:
            conn = sqlite3.connect(db_path)
            catalog = pd.read_sql_query(f"SELECT * FROM {catalog_table}", con=conn)
            self.validate_catalog(catalog)
            self._logger(msg=f"[{self.agent_name}] Create metadata catalog success.", color="green")
        except Exception as e:
            raise ValueError(f"Failed to read catalog table: {catalog_table}, Error: {e}")
        return catalog

    def validate_catalog(self, catalog: pd.DataFrame):
        """"""
        need_columns = ["table", "table_name", "example", "creation_query"]
        not_find_columns = [column for column in need_columns if column not in catalog.columns.to_list()]
        if len(not_find_columns) > 0:
            raise ValueError(f"Catalog table need columns: {not_find_columns}")
        self._logger(msg=f"[{self.agent_name}] Catalog table validate success.", color="green")

    def match_tables(
            self,
            question: str,
            thresh: Optional[float] = 0.8,
            top_n: Optional[int] = 1,
            **kwargs
    ) -> List[MatchTableOutput]:
        """"""
        target = self.catalog["table_name"].tolist()
        matched_data = self.embedding.match(source=[question], target=target, thresh=thresh, top_n=top_n, filter="union")

        matched_tables_lst = []
        if len(matched_data) == 0:
            return matched_tables_lst
        else:
            query_tables = matched_data[0]
            for tab_name, score in zip(query_tables.dst, query_tables.score):
                _table_info = self.catalog[self.catalog["table_name"] == tab_name].to_dict("records")
                if len(_table_info) == 0:
                    self._logger(msg=f"[{self.agent_name}] Not find table: {tab_name} in metadata", color="red")
                else:
                    creation_query = _table_info[0].get("creation_query")
                    example = _table_info[0].get("example")
                    matched_tables_lst.append(MatchTableOutput(
                        table=_table_info[0].get("table"),
                        table_name=tab_name,
                        table_info=f"Creation Query:```\n{creation_query}```\n\nExample:```\n{example}```",
                        score=score,
                    ))
            return matched_tables_lst

    def get_table_info(
            self,
            question: str,
            thresh: Optional[float] = 0.8,
            top_n: Optional[int] = 1,
            **kwargs
    ) -> str:
        """"""
        matched_tables = self.match_tables(question=question, thresh=thresh, top_n=top_n)
        table_info = '\n'.join([tab.table_info for tab in matched_tables])
        return table_info

    def not_find_table_stream(self, task_completion: TaskCompletion) -> TaskCompletion:
        """"""
        self._logger(msg=f"[{self.agent_name}] End, Not find table.", color="red")
        task_completion = self.stream_task_message(
            msg=self.stream_message.not_find_table, task_completion=task_completion)
        return task_completion


class SQLiteTable(SQLiteAgent):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "SQLite Table",
            system_message: Optional[SystemMessage] = PromptSQLite.system_message_table,
            few_shot: Optional[List[Message]] = PromptSQLite.few_shot_table,
            stream: Optional[bool] = False,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.system_message = system_message
        self.few_shot = few_shot
        self.agent_name = agent_name
        self.stream = stream
        self.args = args
        self.kwargs = kwargs

    def _generate_table_name(
            self,
            task_completion: TaskCompletion,
    ) -> str:
        """"""
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)

        messages = self._make_messages(content=task_completion.query)
        self._show_messages(messages, few_shot=False, logger_name=self.agent_name)
        self._trans_generate_stream(self.llm, stream=False)
        completion = self.llm.generate(messages=messages)
        table_name = completion.choices[0].message.content
        self._logger(msg=f"[{self.agent_name}] Table Name: {table_name}", color="green")
        return table_name

    def _match_task_table(
            self,
            query: Union[str, TaskCompletion] = None,
            *args: Any,
            **kwargs: Any,
    ) -> Tuple[str, List[MatchTableOutput], TaskCompletion]:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        table_name = self._generate_table_name(task_completion)
        matched_tables = self.match_tables(
            question=table_name, thresh=kwargs.get("thresh", 0.75), top_n=kwargs.get("top_n", 1))
        return table_name, matched_tables, task_completion

    def _not_find_table(self):
        """"""

    def _find_table_observation(
            self,
            table_name: str,
            matched_tables: List[MatchTableOutput],
            task_completion: TaskCompletion,
    ) -> TaskCompletion:
        """"""
        self._logger(
            msg=f"[{self.agent_name}] Find Tables: {[(tab.table_name, tab.score) for tab in matched_tables]}",
            color='green')
        table_info = '\n'.join([tab.table_info for tab in matched_tables])
        task_completion.content = table_name
        task_completion.observation = table_info
        return task_completion

    def generate(
            self,
            query: Union[str, TaskCompletion] = None,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        table_name, matched_tables, task_completion = self._match_task_table(
            query=query, *args, **kwargs)

        if len(matched_tables) == 0:
            self._logger(msg=f"[{self.agent_name}] End, Not find table.", color="red")
            task_completion.content = self.stream_message.not_find_table
            return task_completion
        else:
            task_completion = self._find_table_observation(table_name, matched_tables, task_completion)
            return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        """"""
        table_name, matched_tables, task_completion = self._match_task_table(
            query=query, *args, **kwargs)

        if len(matched_tables) == 0:
            self._logger(msg=f"[{self.agent_name}] End, Not find table.", color="red")
            task_completion = self.stream_task_message(msg=self.stream_message.not_find_table, task_completion=task_completion)
            yield task_completion
        else:
            task_completion = self._find_table_observation(table_name, matched_tables, task_completion)
            yield task_completion


class SQLiteQA(SQLiteAgent, AgentObservationMixin):
    """"""

    def __init__(
            self,
            agent_name: Optional[str] = "SQLite QA",
            system_message: Optional[SystemMessage] = PromptSQLite.system_message_qa,
            prompt_template: Optional[PromptTemplate] = PromptSQLite.prompt_sqlite_qa,
            stream: Optional[bool] = False,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.system_message = system_message
        self.prompt_template = prompt_template
        self.agent_name = agent_name
        self.stream = stream
        self.args = args
        self.kwargs = kwargs

    def generate(
            self,
            query: Union[str, TaskCompletion] = None,
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        self._logger_agent_start(name=self.agent_name)
        self._logger_agent_question(name=self.agent_name, content=task_completion.query)

        matched_tables = self.match_tables(
            question=task_completion.query, thresh=kwargs.get("thresh", 0.75), top_n=kwargs.get("top_n", 1))
        if len(matched_tables) == 0:
            content = f"[{self.agent_name}] End, Not find table."
            task_completion.content = content
            self._logger(msg=content, color="red")
            return task_completion
        else:
            self._logger(
                msg=f"[{self.agent_name}] Find Tables: {[(tab.table_name, tab.score) for tab in matched_tables]}",
                color='green')
            table_info = '\n'.join([tab.table_info for tab in matched_tables])
            messages = self._make_messages(table_info=table_info, question=query)
            self._show_messages(
                messages=messages, drop_system=True, content_length=None, few_shot=False, logger_name=self.agent_name)
            completion = self.llm.generate(messages=messages)
            task_completion.content = completion.choices[0].message.content
            self._logger(msg=f"[{self.agent_name}] Final Answer: {task_completion.content}", color="yellow")
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

        matched_tables = self.match_tables(
            question=task_completion.query, thresh=kwargs.get("thresh", 0.75), top_n=kwargs.get("top_n", 1))
        if len(matched_tables) == 0:
            yield self.not_find_table_stream(task_completion=task_completion)
        else:
            self._logger(
                msg=f"[{self.agent_name}] Find Tables: {[(tab.table_name, tab.score) for tab in matched_tables]}",
                color='green')
            table_info = '\n'.join([tab.table_info for tab in matched_tables])
            messages = self._make_messages(table_info=table_info, question=query)
            self._show_messages(
                messages=messages, few_shot=False, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
            self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)


class SQLiteScript(AgentScriptMixin, SQLiteAgent):
    """"""

    def __init__(
            self,
            agent_name: Optional[str] = "SQLite Script",
            system_message: Optional[SystemMessage] = PromptSQLite.system_message_query,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = PromptSQLite.prompt_sqlite_query,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            stream_message: Optional[StreamMessage] = StreamMessage(),
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.system_message = system_message
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.agent_name = agent_name
        self.stream_message = stream_message

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

        matched_tables = self.match_tables(
            question=task_completion.query, thresh=kwargs.get("thresh", 0.65), top_n=kwargs.get("top_n", 1))
        if len(matched_tables) == 0:
            yield self.not_find_table_stream(task_completion=task_completion)
        else:
            self._logger(msg=f"[{self.agent_name}] Find Tables: {[(tab.table_name, tab.score) for tab in matched_tables]}", color='green')
            table_info = '\n'.join([tab.table_info for tab in matched_tables])
            messages = self._make_messages(table_info=table_info, question=query)
            self._show_messages(messages=messages, drop_system=True, logger_name=self.agent_name)
            completion = self.llm.generate(messages=messages)
            task_completion.content = completion.choices[0].message.content
            self._logger(msg=f"[{self.agent_name}] Assistant: {task_completion.content}", color="green")

            scripts = ParseCode.sparse_script(string=task_completion.content, script="sql")
            if len(scripts) == 0:
                self._logger(msg=f"[{self.agent_name}] Not Find Script End.\n", color="green")
            else:
                task_completion.script = scripts[0]
                self._logger(msg=f"[{self.agent_name}] Script: ```\n{task_completion.script}\n```", color="magenta")
                task_completion.observation = self.db.run(task_completion.script)
                self._logger(msg=f"[{self.agent_name}] Tools invoke: {task_completion.observation}\n", color="green")
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
        yield self.stream_output(task_completion=task_completion, message=self.stream_message.thinking)

        matched_tables = self.match_tables(
            question=task_completion.query, thresh=kwargs.get("thresh", 0.65), top_n=kwargs.get("top_n", 1))
        if len(matched_tables) == 0:
            yield self.not_find_table_stream(task_completion=task_completion)
        else:
            table_score = [(tab.table_name, round(tab.score, 2)) for tab in matched_tables]
            self._logger(msg=f"[{self.agent_name}] Find Tables: {table_score}", color='green')
            yield self.stream_output(task_completion, message=f"找到最相关的表: {table_score}.\n\n")
            yield self.stream_output(task_completion, message=self.stream_message.write_script)

            table_info = '\n'.join([tab.table_info for tab in matched_tables])
            messages = self._make_messages(table_info=table_info, question=query)
            self._show_messages(messages=messages, drop_system=True, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(
                llm=self.llm, messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
            yield self._new_stream_line(task_completion=task_completion)
            self._logger(msg=f"[{self.agent_name}] Assistant: {task_completion.content}", color="green")
            yield self.stream_output(task_completion, message=self.stream_message.run_script)

            scripts = ParseCode.sparse_script(string=task_completion.content, script="sql")
            if len(scripts) == 0:
                self._logger(msg=f"[{self.agent_name}] Not Find Script End.\n", color="green")
            else:
                task_completion = self._deep_copy_task_completion(task_completion=task_completion, drop_delta=True)
                task_completion.script = scripts[0]
                self._logger(msg=f"[{self.agent_name}] Script: ```\n{task_completion.script}\n```", color="magenta")
                observation = self.db.run(task_completion.script)
                task_completion = self._add_task_completion_observation(
                    task_completion=task_completion, observation=observation)
                self._logger(msg=f"[{self.agent_name}] Tools invoke: {task_completion.observation}\n", color="green")
            yield task_completion


class SQLiteObservation(AgentObservationMixin, SQLiteAgent):
    """"""

    def __init__(
            self,
            agent_name: Optional[str] = "SQLiteAgent-Observation",
            system_message: Optional[SystemMessage] = PromptSQLite.system_message_qa,
            prompt_template: Optional[PromptTemplate] = PromptSQLite.prompt_sqlite_observation,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._clear_prompt()
        self.agent_name = agent_name
        self.system_message = system_message
        self.prompt_template = prompt_template

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self._make_task_completion(query=query, **kwargs)
        yield self.stream_output(task_completion, message=self.stream_message.observation_answer)
        messages = self._make_messages(
            question=task_completion.query, script=task_completion.script, observation=task_completion.observation, )
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

        if task_completion.script is not None:
            messages = self._make_messages(
                question=task_completion.query, script=task_completion.script, observation=task_completion.observation, )
            self._show_messages(messages=messages, logger_name=self.agent_name)
            stream_task_instance = self.stream_task_completion(messages=messages, task_completion=task_completion)
            for task_completion in stream_task_instance:
                yield task_completion
            self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
        else:
            self._logger(msg=f"[{self.agent_name}] Not Find Script.", color="red")
        self._logger_agent_end(name=self.agent_name)


class SQLiteScriptWithObservation(TaskSequence):
    """"""
    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_list = [
            TaskDescription(task=SQLiteScript, task_id=0, task_name="SQLite 脚本"),
            TaskDescription(task=SQLiteObservation, task_id=1, task_name="数据总结"),
        ]


class SQLite(TaskSwitch):
    """"""
    def __init__(
            self,
            task_name: Optional[str] = "Task SQLite",
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.task_list = [
            TaskDescription(
                task=ChatAgent, task_id=0, task_name="数据库介绍机器人",
                task_description="""可以帮助你数据的一般疑问，不可以查询数据，只能够给出对于数据库的一般性介绍。如：数据库中有哪些表？或者一般性的闲聊，如：你是谁？""",
                task_parameters=TaskParameters(
                    few_shot=PromptSQLite.few_shot_chat,
                    system_message=PromptSQLite.system_message_chat,
                )
            ),
            TaskDescription(
                task=SQLiteQA, task_id=1, task_name="数据表介绍机器人",
                task_description="""依据建表语句以及示例数据，介绍表的基本情况。只能给出数据表的一般性介绍，不能查询数据。如：简要介绍工商基本型表。""",
                task_parameters=TaskParameters(
                    verbose=True,
                )
            ),
            TaskDescription(
                task=SQLiteScriptWithObservation, task_id=2, task_name="数据查询机器人",
                task_description="""可以帮助你写SQL语句，并执行观察反馈结果，依据真实的数据回答问题。如：工商基本信息表中有多少数据？""",
                task_parameters=TaskParameters(
                    verbose=True,
                )
            ),
        ]
