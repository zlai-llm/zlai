import os
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Union, ClassVar, Annotated, Literal, Optional, Callable, Iterable

from ..utils import pkg_config
from ..llms import TypeLLM
from ..embedding import TypeEmbedding, Embedding
from ..schema import Message, SystemMessage
from ..prompt import MessagesPrompt
from ..parse import ParseList, ParseDict
from .base import *
from .tasks import TaskSwitch, TaskSequence
from .prompt.fund import *
from .prompt.tasks import TaskDescription, TaskParameters, TaskCompletion


# TODO: 增加名称、fund code、关键词的提取


__all__ = [
    "FundAgent",
    # fund information
    "FundInformationAgent",
    "FundInformation",
    # fund code
    "FundCodeAgent",
    "FundStatus",

]


class FundStatusData(BaseModel):
    """"""
    code: Optional[str] = Field(default=None, description="基金代码")
    name: Optional[str] = Field(default=None, description="基金名称")
    previous_trading_date: Optional[str] = Field(default=None, description="上一交易日")
    net_asset_value: Optional[str] = Field(default=None, description="基金净值（截止上一交易日）")
    estimated_net_asset_value: Optional[str] = Field(default=None, description="估算净值（实时）")
    estimated_return: Optional[str] = Field(default=None, description="估算涨幅（实时）")
    time: Optional[str] = Field(default=None, description="更新时间（实时）")

    @classmethod
    def web2data(cls) -> Dict:
        """"""
        mapping = {
            "fundcode": "code",
            "name": "name",
            "jzrq": "previous_trading_date",
            "dwjz": "net_asset_value",
            "gsz": "estimated_net_asset_value",
            "gszzl": "estimated_return",
            "gztime": "time",
        }
        return mapping

    @classmethod
    def field_desc(cls):
        """"""
        mapping = {key: desc.get("description") for key, desc in cls.model_json_schema()["properties"].items()}
        return mapping


class FundCodeInfo(BaseModel):
    """"""
    code: str = Field("000001", description="基金代码")
    code_name: str = Field("上证指数", description="基金名称")
    score: float = Field(0.0, description="匹配度")


class FundAgent(AgentMixin):
    """"""
    total_funds_columns: List[str] = ['code', 'pinyin_brief', 'name', 'type', 'pinyin']

    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            embedding: Optional[TypeEmbedding] = None,
            agent_name: Optional[str] = "Fund Agent",
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            prompt_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[Message]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            stream: Optional[bool] = False,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
            *args: Any,
            **kwargs: Any,):
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

    def _get_total_funds_info(
            self,
            dtype: Literal["dataframe", "list"] = "list",
    ) -> Union[pd.DataFrame, List[Dict]]:
        """"""
        url = "http://fund.eastmoney.com/js/fundcode_search.js"
        total_funds_info = self._load_url_content(url=url, is_soup=False)
        info = ParseList.greedy_list(total_funds_info)[0]
        df = pd.DataFrame(info, columns=self.total_funds_columns)
        df["code"] = df["code"].astype(str)
        if dtype == "dataframe":
            return df
        elif dtype == "list":
            return df.to_dict("records")
        else:
            raise ValueError(f"dtype must be 'dataframe' or 'list', {dtype}")

    def _get_current_fund_status(
            self,
            code: Annotated[str, '基金代码', True] = '000001',
    ) -> FundStatusData:
        """
        依据用户传入的基金代码，获取当前基金的净值、涨幅等信息。
        """
        url = f"http://fundgz.1234567.com.cn/js/{code}.js"
        fund_status = self._load_url_content(url=url)
        fund_status = ParseDict.eval_dict(string=fund_status)

        if len(fund_status) == 0:
            return FundStatusData()
        else:
            data = {key: fund_status[0].get(origin) for origin, key in FundStatusData.web2data().items()}
            return FundStatusData.model_validate(data)


class FundInformationAgent(FundAgent):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Information Agent",
            system_message: Optional[SystemMessage] = PromptFund.system_message_fund_keyword,
            few_shot: Optional[List[Message]] = PromptFund.few_shot_keyword,
            prompt_template: Optional[PromptTemplate] = PromptFund.prompt_fund_keyword,
            n_fund: int = 5,
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name
        self.system_message = system_message
        self.few_shot = few_shot
        self.prompt_template = prompt_template
        self.n_fund = n_fund
        self.df_total_funds = self._get_total_funds_info(dtype="dataframe")

    def find_fund_info(self, content: str):
        """"""
        df_target = self.df_total_funds[self.df_total_funds["name"].str.contains(content)]
        observation = "\n".join([
            f"一共找到 {len(df_target)} 条相关的基金. 这里仅展示 {self.n_fund} 条记录:",
            df_target.head(self.n_fund).to_markdown(index=False)])
        return observation

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        """"""
        task_completion = self.base_generate(query=query, *args, **kwargs)
        task_completion.observation = self.find_fund_info(content=task_completion.content)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        yield TaskCompletion()


class FundObservation(FundAgent):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Observation",
            system_message: Optional[SystemMessage] = PromptFund.system_message,
            prompt_template: Optional[PromptTemplate] = PromptFund.prompt_fund_observation,
            *args: Any,
            **kwargs: Any
    ):
        """"""
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
        task_completion = self.observation_generate(query=query, *args, **kwargs)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        yield TaskCompletion()


class FundInformation(TaskSequence):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Information",
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name
        self.task_list = [
            TaskDescription(task=FundInformationAgent, task_id=0, task_name="查询代码"),
            TaskDescription(task=FundObservation, task_id=1, task_name="总结回答"),
        ]


class FundCodeAgent(FundAgent):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Code Agent",
            system_message: Optional[SystemMessage] = PromptFund.system_message_fund_code,
            few_shot: Optional[List[Message]] = PromptFund.few_shot_code,
            prompt_template: Optional[PromptTemplate] = PromptFund.prompt_fund_code,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name
        self.system_message = system_message
        self.few_shot = few_shot
        self.prompt_template = prompt_template

    def generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> TaskCompletion:
        task_completion = self.base_generate(query=query, *args, **kwargs)
        task_completion.parsed_data = task_completion.content
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        yield TaskCompletion()


class FundStatusAgent(FundAgent):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Observation",
            system_message: Optional[SystemMessage] = PromptFund.system_message,
            prompt_template: Optional[PromptTemplate] = PromptFund.prompt_fund_observation,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
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
        fund_status = self._get_current_fund_status(code=task_completion.parsed_data)

        if fund_status.net_asset_value is not None and fund_status.time is not None:
            self._logger(msg=f"[{self.agent_name}] Data: {fund_status.model_dump()}\n", color="green")
            task_completion.observation = f"{str(fund_status)}\n\n{str(FundStatusData.field_desc())}"
            task_completion = self.observation_generate(query=task_completion, *args, **kwargs)
        else:
            task_completion.content = f"未找到与{task_completion.parsed_data}有关的基金信息。"
            self._logger_agent_final_answer(name=self.agent_name, content=task_completion.content)
            self._logger_agent_end(name=self.agent_name)
        return task_completion

    def stream_generate(
            self,
            query: Union[str, TaskCompletion],
            *args: Any,
            **kwargs: Any,
    ) -> Iterable[TaskCompletion]:
        yield TaskCompletion()


class FundStatus(TaskSequence):
    """"""
    def __init__(
            self,
            agent_name: Optional[str] = "Fund Information",
            *args: Any,
            **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.agent_name = agent_name
        self.task_list = [
            TaskDescription(task=FundCodeAgent, task_id=0, task_name="查询代码"),
            TaskDescription(task=FundStatusAgent, task_id=1, task_name="总结回答"),
        ]





# class FundAgentBeta(AgentMixin):
#     """"""
#     agent_name: Optional[str]
#     llm: Optional[TypeLLM]
#     embedding: Optional[Embedding]
#     system_message: Optional[SystemMessage]
#     system_template: Optional[PromptTemplate]
#     prompt_template: Optional[PromptTemplate]
#     few_shot: Optional[List[Message]]
#     messages_prompt: Optional[MessagesPrompt]
#     logger: Optional[Callable]
#     verbose: Optional[bool]
#
#     total_funds_columns: List[str] = ['基金代码', '基金拼音简写', '基金名称', '基金类型', '基金拼音全称']
#
#     def __init__(
#             self,
#             llm: Optional[TypeLLM] = None,
#             embedding: Optional[Embedding] = None,
#             system_message: Optional[SystemMessage] = None,
#             system_template: Optional[PromptTemplate] = None,
#             prompt_template: Optional[PromptTemplate] = None,
#             few_shot: Optional[List[Message]] = None,
#             messages_prompt: Optional[MessagesPrompt] = None,
#             agent_name: Optional[str] = "Fund Agent",
#             stream: Optional[bool] = False,
#             logger: Optional[Callable] = None,
#             verbose: Optional[bool] = False,
#     ):
#         self.llm = llm
#         self.embedding = embedding
#         self.system_message = system_message
#         self.system_template = system_template
#         self.prompt_template = prompt_template
#         self.few_shot = few_shot
#         self.messages_prompt = messages_prompt
#
#         self.agent_name = agent_name
#         self.stream = stream
#         self.logger = logger
#         self.verbose = verbose
#
#     def create_cache(self, cache_file_path: str):
#         """"""
#         self._logger(msg="Not find total funds list. start reloading cache ...\n", color="green")
#         df_total_funds = self.get_total_funds(dtype="dataframe")
#         df_total_funds["vector"] = self.embedding.embedding(tuple(df_total_funds["基金名称"].to_list())).to_list()
#         self._save_json_table(df=df_total_funds, save_path=cache_file_path)
#         self._logger(msg=f"Funds cache created, total funds: {len(df_total_funds)}\n", color="blue")
#
#     def reset_cache(self, cache_file_path: str):
#         """"""
#         self.create_cache(cache_file_path=cache_file_path)
#
#     def update_cache(self, cache_file_path: str,):
#         """"""
#         if not os.path.exists(cache_file_path):
#             self.create_cache(cache_file_path=cache_file_path)
#         else:
#             new_data = self.get_total_funds(dtype="list")
#             # cache_data = pd.read_json(cache_file_path, orient="records")
#             cache_data = self._load_json_table(cache_file_path)#pd.read_json(cache_file_path, orient="records")
#             self._logger(msg=f"load new data: {len(new_data)}; cache data: {len(cache_data)}", color="green")
#
#             need_update = [item for item in new_data if item.get("基金代码") not in cache_data["基金代码"].to_list()]
#
#             if len(need_update) > 0:
#                 self._logger(msg=f"Found {len(need_update)} new funds, start updating cache ...\n", color="green")
#                 df_need_update = pd.DataFrame(need_update, columns=self.total_funds_columns)
#                 update_funds_name = df_need_update["基金名称"].to_list()
#                 df_need_update["vector"] = self.embedding.embedding(text=tuple(update_funds_name)).to_list()
#                 df_cache_data = pd.concat(objs=[cache_data, df_need_update], axis=0)
#                 self._save_json_table(df=df_cache_data, save_path=cache_file_path)
#                 self._logger(msg=f"Update success, total funds: {len(df_cache_data)}\n", color="blue")
#             else:
#                 self._logger(msg=f"Not find new data.", color="green")
#
#     def validate_cache_vector(self, cache_file_path: str):
#         """ validate cache vector is correct """
#         cache_data = self._load_json_table(path=cache_file_path).to_dict("records")[0]
#         cache_vector = np.array([cache_data.get("vector")])
#         vector = self.embedding.embedding(text=tuple([cache_data.get("基金名称")])).to_numpy()
#         matrix = self.embedding._similarity_matrix(source_vector=cache_vector, target_vector=vector)
#         if matrix[0][0] < 0.98:
#             raise ValueError(f"Cache vector is not correct, {matrix[0][0]}")
#         else:
#             self._logger(msg=f"vector correct, score: {matrix[0][0]: .2f}", color="green")
#
#     def validate_cache(self, folder="agent_fund", file_name="total_funds.json"):
#         """"""
#         folder_path = os.path.join(pkg_config.cache_path, folder)
#         file_path = os.path.join(pkg_config.cache_path, folder, file_name)
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path, exist_ok=True)
#
#         if not os.path.exists(file_path):
#             self.create_cache(cache_file_path=file_path)
#         else:
#             self._logger(msg=f"Find cache file: {file_path} exist. Start validate cache data.\n", color="green")
#             self.validate_cache_vector(cache_file_path=file_path)
#             self.update_cache(cache_file_path=file_path)
#
#     def get_total_funds(
#             self,
#             dtype: Literal["dataframe", "list"] = "list",
#     ) -> Union[pd.DataFrame, List[Dict]]:
#         """"""
#         return self._get_total_funds_info(dtype=dtype)
#
#     def match_funds(self, query, top_n: int = 1) -> List[Dict]:
#         funds_name_lst = [fund.get("基金名称", "") for fund in self.total_funds]
#         matched_fund_idx = self.embedding.match_idx(source=[query], target=funds_name_lst, top_n=top_n)[0]
#         return [self.total_funds[_id] for _id in matched_fund_idx]
#
#     def _save_json_table(self, df: pd.DataFrame, save_path: str):
#         """"""
#         df["基金代码"] = df["基金代码"].astype(str)
#         if df["基金代码"].str.len().min() < 6:
#             raise ValueError(f"new fund code error.")
#         df.to_json(save_path, orient="records")
#
#     def _load_json_table(self, path: str) -> pd.DataFrame:
#         """"""
#         df = pd.read_json(path, orient="records", dtype={'基金代码': str})
#         return df
#
#     def find_total_funds(
#             self,
#             fund_name: Annotated[str, '基金名称', True],
#             head: int = 5,
#     ) -> Dict:
#         """
#         依据用户传入的基金名称，获取基金代码、基金拼音简写、基金类型、基金拼音全称等信息
#         """
#         df = self._get_total_funds_info(dtype="dataframe")
#         data = df[df["基金名称"].str.contains(fund_name)].head(head).to_dict("records")
#         return data
#
#     def find_fund_basic_info(
#             self,
#             fund_code: Annotated[str, '基金代码', True] = '000001',
#     ) -> Dict:
#         """
#         依据用户传入的基金代码，获取基金的基本信息。
#         """
#         url = f"https://fundf10.eastmoney.com/jbgk_{fund_code}.html"
#         soup = self._load_url_content(url=url, features="lxml", is_soup=True)
#         table_info = soup.find_all('table', {'class': 'info w790'})[0]
#         th = [item.text for item in table_info.find_all('th')]
#         td = [item.text for item in table_info.find_all('td')]
#         fund_basic_info = dict(zip(th, td))
#         return fund_basic_info
#
#     def generate(
#             self,
#             query: Union[str, TaskCompletion],
#             *args: Any,
#             **kwargs: Any,
#     ) -> TaskCompletion:
#         """"""
#         message = self._make_messages(query=query)
#         self._show_messages(messages=[], logger_name=self.agent_name)
#         completion = self.llm.generate(messages=message)
#         return completion.choices[0].message.content
#
