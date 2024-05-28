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
    "register_tool",
    "dispatch_tool",
    "get_tools",
    "AgentOutput",
    "BaseAgent",
]


class ToolMessage(BaseModel):
    """"""
    role: str = "tool"
    content: Optional[str] = None
    tool_call_id: Optional[str] = None


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
    observation: ToolMessage = ToolMessage(content='', tool_call_id=None)
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


class ToolParameters(BaseModel):
    """"""
    type: str = "object"
    properties: Dict[str, Dict]
    required: List[str]


class ToolFunction(BaseModel):
    """"""
    name: str
    description: str
    parameters: ToolParameters


class ToolItem(BaseModel):
    type: str = "function"
    function: ToolFunction


def enum_metadata(typ: EnumMeta) -> Dict:
    """"""
    enum_typ_lst = list(typ)
    enum_properties = dict()
    info = dict()
    for item in enum_typ_lst:
        enum_item = eval(item.value)
        enum_typ, (enum_desc, enum_name) = enum_item.__origin__, enum_item.__metadata__
        enum_properties.update({"type": enum_typ.__name__,})
        info.update({"value": enum_name, "description": enum_desc})
    enum_properties.update({"enum": info})
    return enum_properties


def register_tool(tool_hooks: Dict, tool_descriptions: List):
    """"""
    def decorator_func(func):
        tool_name = func.__name__
        tool_description = inspect.getdoc(func).strip()
        python_params = inspect.signature(func).parameters
        tool_params = []
        required_lst = []
        properties = dict()
        for name, param in python_params.items():
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                raise TypeError(f"Parameter `{name}` missing type annotation")
            if get_origin(annotation) != Annotated:
                raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")

            typ, (description, required) = annotation.__origin__, annotation.__metadata__

            if isinstance(typ, EnumMeta):
                enum_properties = enum_metadata(typ)
            else:
                enum_properties = None

            typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
            if not isinstance(description, str):
                raise TypeError(f"Description for `{name}` must be a string")
            if not isinstance(required, bool):
                raise TypeError(f"Required for `{name}` must be a bool")

            if required:
                required_lst.append(name)

            tool_params.append({
                "name": name,
                "description": description,
                "type": typ,
                "required": required
            })

            properties.update({name: dict()})
            properties.get(name).update({
                "description": description,
                "type": typ,
            })
            if enum_properties:
                properties.get(name).update({
                    "enum": enum_properties.get("enum"),
                    "type": enum_properties.get("type"),
                })

        tool_def = {
            "name": tool_name,
            "description": tool_description,
            "parameters": tool_params
        }
        tool_hooks[tool_name] = func

        tool_parameters = ToolParameters(
            properties=properties,
            required=required_lst,
        )
        tool_item = ToolItem(
            function=ToolFunction(
                name=tool_def.get("name"),
                description=tool_def.get("description"),
                parameters=tool_parameters
            )
        )

        tool_descriptions.append(tool_item.model_dump())

        def wrapper(*args, **kwargs):
            """"""
            return func
        return wrapper
    return decorator_func


def dispatch_tool(
        tool_name: str,
        tool_params: dict,
        hooks: Optional[Dict[str, Callable]] = None
) -> str:
    if hooks is None:
        hooks = _TOOL_HOOKS
    if tool_name not in hooks:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = hooks[tool_name]
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)


def get_tools() -> List[dict]:
    return deepcopy(_TOOL_DESCRIPTIONS)


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

