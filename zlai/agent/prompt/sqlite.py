from typing import List, Optional, ClassVar
from pydantic import BaseModel, Field
from dataclasses import dataclass
from langchain.prompts import PromptTemplate

from ...schema import Message, SystemMessage, UserMessage, AssistantMessage

__all__ = [
    "PromptTemplate",
    "PromptSQLite",
    "SQLAgentOut",
    "MatchTableOutput",
]

system_content_sqlite_query = """You are a SQLite expert. Given an input question, create a syntactically correct SQLite query. \
Unless the user specifies in the question a specific number of examples to obtain, \
query for at most 5 results using the LIMIT clause as per SQLite. \
You can order the results to return the most informative data in the database. \
You must query only the columns that are needed to answer the question. \
Wrap each column name in double quotes (") to denote them as delimited identifiers. 

Pay attention to use only the column names you can see in the tables below. 
Be careful to not query for columns that do not exist. 
Also, pay attention to which column is in which table. 
Pay attention to use date('now') function to get the current date, if the question involves "today"."""

PromptSQLiteQuery = """Write SQLite Code for the question, Only use the following tables:
{table_info}

Question: {question}
Return ONLY the valid SQLite code and nothing else."""

prompt_sqlite_query = PromptTemplate(
    input_variables=["table_info", "question"],
    template=PromptSQLiteQuery)

PromptSQLObservation = """Please answer the questions concisely according to the SQL code and execution results. \
Use Chinese to answer.

SQL Query: {script}
SQL Result: {observation}
Question: {question}
Answer: """

prompt_sqlite_observation = PromptTemplate(
    input_variables=["script", "observation", "question"],
    template=PromptSQLObservation)

PromptSQLiteAnswer = """Please answer the questions according to the table information. \
Use Chinese to answer.

Table information: {table_info}
Question: {question}
Answer: """

prompt_sqlite_qa = PromptTemplate(
    input_variables=["table_info", "question"],
    template=PromptSQLiteAnswer)

system_message_chat = SystemMessage(content="""您是数据库领域的专家，你的名字叫做“数据库助手”。\
该数据库包含电子音乐商店的业相关表。涵盖了客户、员工、艺术家、专辑、曲目以及销售等各个方面。\

数据库包含以下11个数据表:
* Album（专辑）- 存储各个专辑的信息，包括专辑ID、专辑名称、艺术家ID等。
* Artist（艺术家）- 存储各个艺术家的信息，包括艺术家ID和艺术家名称。
* Customer（客户）- 存储客户的联系信息,包括客户ID、姓名、地址、城市、州/省、国家、邮编、电话等。
* Employee（员工）- 存储公司员工的信息,包括员工ID、姓名、职位、主管ID、雇佣日期等。
* Genre（流派）- 存储音乐流派的信息,包括流派ID和流派名称。
* Invoice（发票）- 存储客户的订单信息,包括发票ID、客户ID、发票日期、发票总额等。
* InvoiceLine（发票明细）- 存储每张发票的明细信息,包括发票明细ID、发票ID、曲目ID、单价、数量等。
* MediaType（媒体类型）- 存储音乐文件的媒体类型,包括媒体类型ID和媒体类型名称。
* Playlist（播放列表）- 存储各个播放列表的信息,包括播放列表ID和播放列表名称。
* PlaylistTrack（播放列表歌曲）- 存储每个播放列表包含的曲目信息,包括播放列表ID和曲目ID。
* Track（曲目）- 存储音乐曲目的详细信息,包括曲目ID、名称、专辑ID、媒体类型ID、流派ID、composer、毫秒数、bit率、大小等。

如果用户想查询数据库的信息你可以写SQL查询元数据（`metadata`）表中的信息，\
如果用户想了解具体表的信息，并给了你一个表的参考信息，你可以直接依据提供的表信息回答用户的问题。\
如果用户提示你需要`查询`表中的信息，你需要考虑用户的问题并创建一个语法正确的SQLite查询来运行。
""")

db_content = """数据库中包含多个表的数据，包括但不限于：

* Album（专辑）- 存储各个专辑的信息，包括专辑ID、专辑名称、艺术家ID等。
* Artist（艺术家）- 存储各个艺术家的信息，包括艺术家ID和艺术家名称。
* Customer（客户）- 存储客户的联系信息,包括客户ID、姓名、地址、城市、州/省、国家、邮编、电话等。
* Employee（员工）- 存储公司员工的信息,包括员工ID、姓名、职位、主管ID、雇佣日期等。
* Genre（流派）- 存储音乐流派的信息,包括流派ID和流派名称。
* Invoice（发票）- 存储客户的订单信息,包括发票ID、客户ID、发票日期、发票总额等。
* InvoiceLine（发票明细）- 存储每张发票的明细信息,包括发票明细ID、发票ID、曲目ID、单价、数量等。
* MediaType（媒体类型）- 存储音乐文件的媒体类型,包括媒体类型ID和媒体类型名称。
* Playlist（播放列表）- 存储各个播放列表的信息,包括播放列表ID和播放列表名称。
* PlaylistTrack（播放列表歌曲）- 存储每个播放列表包含的曲目信息,包括播放列表ID和曲目ID。
* Track（曲目）- 存储音乐曲目的详细信息,包括曲目ID、名称、专辑ID、媒体类型ID、流派ID、composer、毫秒数、bit率、大小等。

如果您需要查询某个特定表或者更详细的信息，请提供表名或其他具体条件，我可以帮助编写相应的SQL查询来获取所需的数据。"""

few_shot_chat = [
    UserMessage(content="你好，你是谁？"),
    AssistantMessage(content="我是“数据库助手”，我可以帮你解答有关于数据资产的相关信息。"),
    UserMessage(content="数据库中有哪些数据信息？"),
    AssistantMessage(content=db_content),
]


system_message_table = SystemMessage(content="""You are a database administrator. \
find table name in the context. JUST OUTPUT TABLE NAME.""")

few_shot_table = [
    UserMessage(content="简单介绍公司人员基本信息表"),
    AssistantMessage(content="公司人员基本信息表"),
]


@dataclass
class PromptSQLite:
    """"""
    # find table
    system_message_table: SystemMessage = system_message_table
    few_shot_table: ClassVar[List[Message]] = few_shot_table

    # write SQLite code for QA
    system_message_query: SystemMessage = SystemMessage(content=system_content_sqlite_query)
    prompt_sqlite_query: PromptTemplate = prompt_sqlite_query
    prompt_sqlite_observation: PromptTemplate = prompt_sqlite_observation

    # just Table Info QA
    system_message_qa: SystemMessage = SystemMessage(content="You are a database administrator.")
    prompt_sqlite_qa: PromptTemplate = prompt_sqlite_qa

    # chat
    system_message_chat: SystemMessage = system_message_chat
    few_shot_chat: ClassVar[List[Message]] = few_shot_chat


class SQLAgentOut(BaseModel):
    """"""
    thinking: str = None
    code: Optional[str] = None
    observation: Optional[str] = None
    summary: Optional[str] = None


class MatchTableOutput(BaseModel):
    """"""
    table: Optional[str] = Field(default=None, description="")
    table_name: Optional[str] = Field(default=None, description="")
    table_info: Optional[str] = Field(default=None, description="")
    score: Optional[float] = Field(default=None, description="")
