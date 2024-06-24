import io
import sys
import typing
import inspect
import logging
import traceback
from enum import EnumMeta

import pandas as pd
from pydantic import BaseModel
from copy import deepcopy
from typing import *
from types import GenericAlias

from ..utils import log, LoggerMixin
from ..parse import sparse_query
from ..schema import *
from ..llms import *

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = []


__all__ = [
    "AgentOutput",
    "BaseAgent",
]


class BaseAgent(LoggerMixin):
    """"""
    API_CLASS: TypeLLM
    tools: List = []
    llm: TypeLLM
    api_key_path: Optional[str] = None
    messages: List[Message] = []
    tool_name: str = ''
    tool_params: Dict = dict()
    dispatch_fun: Optional[Callable] = None
    observation: ToolsMessage = ToolsMessage(content='', tool_call_id=None)
    tool_call_id: str = ''
    verbose: bool = True
    stream: Optional[bool] = False
    code: Optional[str] = None
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            llm: Optional[LocalLLMAPI],
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """"""
        self.llm = llm
        self.logger = logger
        self.verbose = verbose

    def __call__(
            self,
            prompt,
            *args, **kwargs):
        """"""
        self.call_tool(prompt=prompt)
        self.dispatch_tool()
        self.add_observation()
        output = self.observation_summary()
        return output

    def set_remote_llm(
            self,
            remote,
            api_key_path,
            gen_config: Optional[GenerateConfig] = None,
            model_name: ModelName = ZhipuModel.glm_3_turbo,
            is_message_cache: Optional[bool] = False,
    ):
        """"""
        self.llm = self.API_CLASS(
            remote=remote,
            api_key_path=api_key_path,
            is_message_cache=is_message_cache,
            verbose=self.verbose,
        )

        if not gen_config:
            gen_config = ZhipuGenerateConfig(
                model_name=model_name,
                tools=self.tools,
                tool_choice='auto',
            )
        self.llm.set_generate_config(config=gen_config)

    def set_local_llm(self):
        """"""
        self.llm = self.API_CLASS()

    def set_llm(
            self,
            remote,
            api_key_path,
            gen_config: Optional[GenerateConfig] = None,
            model_name: ModelName = ZhipuModel.glm_3_turbo,
            is_message_cache: Optional[bool] = False,
    ):
        """"""
        self.set_remote_llm(
            remote=remote,
            api_key_path=api_key_path,
            gen_config=gen_config,
            model_name=model_name,
            is_message_cache=is_message_cache,
        )

    def execute(
            self,
            df: pd.DataFrame,
            query: str
    ) -> str:
        """"""
        stdout_backup = sys.stdout
        sys.stdout = io.StringIO()
        exec(query)
        output = sys.stdout.getvalue()
        sys.stdout = stdout_backup
        return output

    def dispatch_tool(self):
        """"""
        observation = self.dispatch_fun(
            tool_name=self.tool_name,
            tool_params=self.tool_params,
        )
        if self.verbose: print(observation)
        self.observation.content = observation
        self.observation.tool_call_id = self.tool_call_id

    def add_observation(self):
        """"""
        self.messages.append(self.observation.model_dump())

    def call_message(
            self,
            query: str,
            query_type='python',
            log_info: str = 'LLM Message:',
    ) -> Union[Tuple[CompletionMessage, str]]:
        """"""
        self.messages.append(Message(content=query))
        completion = self.llm.generate(messages=self.messages)
        completion_message = completion.choices[0].message
        self.messages.append(completion_message)
        if self.verbose:
            log(f"""{log_info}\n {completion_message.content}\n""")

        code = None
        if query_type:
            code = sparse_query(string=completion_message.content, query_type=query_type)
            self.code = code
            if self.verbose:
                log(f"""Sparse Code ... \n {self.code}\n""")
        return completion_message, code

    def call_message_stream(
            self,
            query: str,
            query_type='python',
            log_info: str = 'LLM Message:',
    ) -> Union[Tuple[Completion, str]]:
        """"""
        self.messages.append(UserMessage(content=query))

        assistant_content = ""
        for completion in self.llm.generate(messages=self.messages):
            if self.llm.generate_config.incremental:
                assistant_content += completion.choices[0].message.content
            else:
                assistant_content = completion.choices[0].message.content
            yield completion, None

        self.messages.append(AssistantMessage(content=assistant_content))
        self._logger(msg=f"""{log_info}\n {assistant_content}\n""")

        if query_type:
            code = sparse_query(string=assistant_content, query_type=query_type)
            self.code = code
            self._logger(msg=f"""Sparse Code ... \n {self.code}\n""")
            yield None, code

    def call_tool(self, message: List[Message]):
        """"""
        self.messages.extend(message)
        completion = self.llm.generate(messages=self.messages)

        if self.verbose:
            log(f"""Agent response: {completion.tool_calls[0]}\n""")

        self.messages.append(completion)
        try:
            self.tool_name = completion.tool_calls[0].function.name
            self.tool_params = eval(completion.tool_calls[0].function.arguments)
            self.tool_call_id = completion.tool_calls[0].id
            if self.verbose:
                log(f"""Call Function: {self.tool_name}\nParams: {self.tool_params}\n""")
        except Exception as e:
            logging.warning(f"ERROR: {e}. messages: {self.messages}\n")

    def observation_summary(self):
        """"""
        print(f"Stream: {self.stream}")
        if self.stream:
            self.llm.generate_config.update({'stream': self.stream})

            print(f'STREAM: {self.llm.generate_config.get("stream")}')
            return self.llm.generate(messages=self.messages)
        else:
            response = self.llm.generate(messages=self.messages)
            return response


class AgentOutput(BaseModel):
    """"""
    def mapping_data(self):
        """"""
        name = self.model_fields.keys()
        desc = [item.description for item in self.model_fields.values()]
        return name, desc

    def desc2name(self):
        """"""
        name, desc = self.mapping_data()
        return dict(tuple(zip(desc, name)))

    def name2desc(self):
        """"""
        name, desc = self.mapping_data()
        return dict(tuple(zip(name, desc)))

    def map_dict(self):
        """"""
        output = dict()
        mapping = self.name2desc()
        for k, v in self.model_dump().items():
            output[mapping[k]] = v
        return output
