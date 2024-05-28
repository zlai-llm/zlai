import pandas as pd
from pydantic import BaseModel
from typing import *
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase

from ..utils import log
from ..schema import *
from ..embedding import *
from ..parse import sparse_query
from .agent import *


__all__ = [
    "SystemTemplate",
    "SQLAgent",
]


PromptSQLite = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today". Answer in Chinese.

SQL Query format as follow:
```sql
... Some SQL CODE ...
```

Only use the following tables:
{table_info}

Question: {question}
SQLQuery or Answer:
"""

PromptSQLAnswer = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """

SystemTemplate = """您是SQLite专家。你需要考虑用户的问题并创建一个语法正确的SQLite查询来运行。
除非用户在问题中指定了要获得的特定数量的示例，否则根据SQLite使用LIMIT子句最多查询5个结果。您可以对结果进行排序，以返回数据库中信息量最大的数据。
请注意只使用下表中可以看到的列名。请注意不要查询不存在的列。此外，还要注意哪个列在哪个表中。如果问题涉及“今天”，请注意使用日期（'now'）函数来获取当前日期。
如果用户提出的问题可以直接使用表信息回答，请直接回答，如`数据每日新增量级/存量存储量/数据存量量级`等信息。否则，请创建一个语法正确的SQLite查询来运行。

```sql
... Some SQL code ...
```

表信息如下：
{table_info}
"""

prompt_sqlite = PromptTemplate(
    input_variables=["table_info", "question"],
    template=SystemTemplate)

prompt_answer = PromptTemplate(
    input_variables=["question", "query", "result"],
    template=PromptSQLAnswer)


class SQLAgentOut(BaseModel):
    """"""
    thinking: str = None
    code: Optional[str] = None
    observation: Optional[str] = None
    summary: Optional[str] = None


class MatchTableInfo(BaseModel):
    """"""
    table_name: str
    table_info: str
    match_info: List[EmbeddingMatchOutput]


class SQLAgent(BaseAgent):
    """"""
    embedding: Embedding
    # messages: List[Message] = []

    def __init__(
            self,
            db: SQLDatabase,
            llm: LocalModel = None,
            catalog: Optional[pd.DataFrame] = None,
            stream: Optional[bool] = False,
            verbose: Optional[bool] = True,
            logger: Optional[Callable] = None,
    ):
        super().__init__(llm=llm, verbose=verbose, logger=logger)
        self.db = db
        self.verbose = verbose
        self.stream = stream
        self.catalog = catalog
        self.dialect = db.dialect
        self.table_info = db.get_table_info()
        self.messages = []

    def __call__(
            self,
            query: str,
            stream: bool,
            thinking_prompt: Optional[PromptTemplate] = None,
            *args, **kwargs
    ) -> Union[str, SQLAgentOut]:
        """"""
        if stream:
            return self.call_agent_stream(question=query, thinking_prompt=thinking_prompt)
        else:
            return self.call_agent_message(question=query, thinking_prompt=thinking_prompt)

    def set_system_message(
            self,
            template: str,
            input_variables: List[str] = ["table_info", ],
            reset=True,
            **kwargs: Any
    ):
        """"""
        if reset:
            self.messages = []
        prompt_system = PromptTemplate(
            input_variables=input_variables,
            template=template)
        system_message = SystemMessage(content=prompt_system.format(**kwargs))
        self.messages.append(system_message)

    def match_table(self, query) -> MatchTableInfo:
        """"""
        embedding = Embedding(
            emb_url=EMBUrl.bge_m3,
            max_len=512,
            max_len_error='split',
            batch_size=10,
        )
        match_data = embedding.match(target=self.catalog.dimension.tolist(), source=[query], top_n=1)[0]

        mapping = {
            "表名": "table_name",
            "数据模块": "module",
            "数据维度": "dimension",
            "数据列名": "columns",
            "数据列描述": "columns_desc",
            "数据样例": "example",
            "涉及企业数": "table_companies",
            "数据存量量级": "data_volume",
            "数据每日新增量级": "daily_update_volume",
            "存量存储量": "stock_storage",
            "建表语句": "creation_query",
            "时间": "time",
        }

        name2desc = {val: key for key, val in mapping.items()}
        table = self.catalog[self.catalog.dimension == match_data.dst[0]].to_dict("records")[0]

        append_list = ["daily_update_volume", "stock_storage", "data_volume", "table_companies"]
        table_append_info = {name2desc.get(item): table.get(item) for item in append_list}

        table_name = table.get("dimension")
        example = table.get("example")
        creation_query = table.get("creation_query")

        table_info = f"{creation_query}\n\n{example}\n\n补充信息：\n{table_append_info}"
        return MatchTableInfo(
            table_name=table_name, table_info=table_info, match_info=[match_data],
        )

    def call_agent_message(
            self,
            question: str,
            thinking_prompt: Optional[PromptTemplate] = prompt_sqlite,
    ) -> SQLAgentOut:
        """"""
        # thinking
        if thinking_prompt:
            thinking_prompt = prompt_sqlite.format_prompt(
                table_info=self.table_info, question=question
            ).to_string()
        else:
            thinking_prompt = question

        thinking_message, code = self.call_message(query=thinking_prompt, query_type='sql', log_info='Thinking ...')

        if code:
            # execute
            observation = self.execute_sql()
            if self.verbose: log(f"Observation ...\n  {observation}.")

            # summary
            summary_prompt = prompt_answer.format_prompt(
                question=question,
                query=code,
                result=observation,
            ).to_string()
            summary_message, _ = self.call_message(query=summary_prompt, query_type=None, log_info='Summarizing ...')
        else:
            observation = None
            summary_message = CompletionMessage(role='assistant')
        return SQLAgentOut(
            thinking=thinking_message.content,
            code=code,
            observation=observation,
            summary=summary_message.content,
        )

    def call_agent_stream(
            self,
            question: str,
            thinking_prompt: Optional[PromptTemplate] = None,
    ) -> str:
        """"""
        match_table_info = self.match_table(query=question)
        table_info, table_name = match_table_info.table_info, match_table_info.table_name

        if match_table_info.match_info[0].score[0] <= 0.6:
            yield constant_completion(content=f"未找到相关表信息...\n\n")
        else:
            self.set_system_message(template=SystemTemplate, input_variables=["table_info"], table_info=table_info, reset=True,)
            yield constant_completion(content=f"找到最相关的表：{table_name}\n\n")
            code = None

            # thinking
            if thinking_prompt:
                thinking_prompt = prompt_sqlite.format_prompt(
                    table_info=table_info, question=question
                ).to_string()
            else:
                thinking_prompt = question

            for thinking_completion, code in self.call_message_stream(
                    query=thinking_prompt, query_type='sql', log_info='Thinking ...'):
                yield thinking_completion

            if code:
                self._logger(msg=f"执行SQL:\n```sql\n{code}```\n\n")
                yield constant_completion(content=f"\n\n执行SQL代码...\n\n")

                # execute
                observation = self.execute_sql()
                self._logger(msg=f"Observation ...\n  {observation}.")
                yield constant_completion(content=f"执行结果:\n```\n{observation}\n```\n\n")

                # summary
                summary_prompt = prompt_answer.format_prompt(
                    question=question,
                    query=code,
                    result=observation,
                ).to_string()

                self.messages.append(UserMessage(content=summary_prompt))
                yield constant_completion(content=f"\n最终回答：\n")

                summary_completion = None
                for i, summary_completion in enumerate(self.llm.generate(messages=self.messages)):
                    yield summary_completion

                if summary_completion:
                    self.messages.append(summary_completion.choices[0].message)

    def execute_sql(self):
        """"""
        try:
            return self.db.run(self.code)
        except Exception as error:
            return f"执行SQL代码时发生错误：{error}"
