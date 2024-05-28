from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Union, Any, Optional, Callable, Literal

from ..utils.mixin import *
from ..schema import ZhipuModel, LLMUrl, Message
from ..llms import LocalLLMAPI, Zhipu
from ..parse import ParseString
from ..prompt import MessagesPrompt


__all__ = [
    "InvokeExtract",
    "ExtractConfig",
    "ModelGroupConfig",
]

_parse_type = Literal["greedy_list", "eval_list", "nested_list", "greedy_dict", "eval_dict", "nested_dict"]


class ExtractConfig(BaseModel):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    prompt: List[Any] = []
    model_name: Union[str, ZhipuModel, LLMUrl, None] = None
    temperature: float = 0.9
    top_p: float = 0.7
    do_sample: bool = True
    max_tokens: Optional[int] = 512


class ModelGroupConfig(BaseModel):
    """"""
    TEXT_PREPARE_CLASS: Callable
    SELECT_FUN_STR: str
    PROMPT_CLASS: Callable
    extract_config: ExtractConfig
    is_warp_user_content: bool = False


class InvokeExtract(LoggerMixin):
    """"""
    # model
    llm: Union[LocalLLMAPI, Zhipu]
    messages_prompt: MessagesPrompt
    # content
    text_prepare: Optional[Callable]
    # parse
    parse_fun: Optional[Callable] = None
    parse_type: Optional[_parse_type] = 'eval_dict'
    # logger
    verbose: Optional[bool]
    logger: Optional[Callable]

    def __init__(
            self,
            llm: Union[LocalLLMAPI, Zhipu],
            messages_prompt: MessagesPrompt,
            text_prepare: Optional[Callable] = None,
            parse_fun: Optional[Callable] = None,
            parse_type: Optional[_parse_type] = None,
            verbose: Optional[bool] = None,
            logger: Optional[Callable] = None,
    ):
        """

        :param llm:
        :param messages_prompt:
        :param text_prepare:
        :param parse_fun:
        :param parse_type: "greedy_list", "eval_list", "nested_list", "greedy_dict", "eval_dict", "nested_dict"
        :param verbose:
        :param logger:
        """
        self.llm = llm
        self.messages_prompt = messages_prompt
        self.text_prepare = text_prepare
        self.parse_fun = parse_fun
        self.parse_type = parse_type
        self.verbose = verbose
        self.logger = logger

    def invoke(
            self,
            messages: List[Message],
    ) -> Union[str, None]:
        """"""
        try:
            self._logger(msg=f"Generate config:", color="green")
            self._logger_dict(msg=self.llm.generate_config.model_dump(), color="green")
            response = self.llm.generate(messages=messages)
            self._logger(msg=f"LLM response info: {response}", color="green")
            content = response.choices[0].message.content
            return content
        except Exception as e:
            error_message = f"Remote API error: {e}\nMessages: {[message.model_dump() for message in messages]}"
            self._logger(msg=error_message, color="red")
            return None

    def parse_response_content(self, content: str) -> Any:
        """"""
        parse = ParseString()
        if self.parse_type:
            parse_func = getattr(parse, self.parse_type)
            parsed_response = parse_func(content)
        elif self.parse_fun is not None:
            parsed_response = parse.udf_parse(func=self.parse_fun, content=content)
        else:
            raise ValueError(f"Please set parse_type or parse_fun")
        self._logger(msg=f"Parse response content: {parsed_response};\nerror message: {parse.sparse_error}", color="green")
        return parsed_response

    def _make_schema_output(self, parsed_data: Dict, schema: Optional[Any] = None, schema_keys: List[str] = None) -> Any:
        """"""
        data = dict()

        if schema_keys is None:
            schema_keys = [schema_key for schema_key, _ in schema.model_json_schema()["properties"].items()]

        for schema_key, schema_property in schema.model_json_schema()["properties"].items():
            if schema_key in schema_keys:
                description = schema_property.get("description")
                default = schema_property.get("default")
                if description is not None:
                    val = parsed_data.get(description, default)
                    data.update({schema_key: val})
        return schema.model_validate(data)

    def _make_output(self, answer: str, schema: Optional[Any] = None, **kwargs) -> Union[str, BaseModel, None]:
        """"""
        if answer is not None:
            parsed_answer = self.parse_response_content(content=answer)
            if schema:
                return self._make_schema_output(parsed_data=parsed_answer[0], schema=schema, **kwargs)
            else:
                return parsed_answer
        else:
            return None

    def extract(
            self,
            content: str,
            schema: Optional[Any] = None,
            **kwargs,
    ) -> Union[Dict, List, str, None, Any]:
        """"""
        self._logger(msg=f"Start extract content: {content[:50]}", color="green")
        # clean content
        if self.text_prepare is not None:
            cleand_content = self.text_prepare(content=content)
        else:
            cleand_content = content
        # create messages
        messages = self.messages_prompt.prompt_format(content=cleand_content)
        answer = self.invoke(messages=messages)
        return self._make_output(answer=answer, schema=schema, **kwargs)
