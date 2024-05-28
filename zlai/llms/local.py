from typing import (
    Union, List, Dict, Any, Callable,
    Iterable, Literal, Optional)
from ..schema import *
from ..utils import LoggerMixin
from .base import *
from .generate import *


__all__ = [
    "LocalLLMAPI"
]


class LocalLLMAPI(Generate, LoggerMixin):
    """
    TODO: Message要增加当次的Prompt/query或History
    """
    model_name: Union[Model, str]
    messages: Optional[List[Message]]
    generate_config: Optional[GenerateConfig]
    llm_request: LLMRequest
    parse_info: List[ParseInfo] = []
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            generate_config: Optional[GenerateConfig] = None,
            output: Literal["completion", "message", "str"] = "completion",
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """"""
        self.model_name = generate_config.model
        self.generate_config = generate_config
        self.logger = logger
        self.verbose = verbose
        self.llm_request = LLMRequest(
            model_name=self.model_name,
            generate_config=generate_config,
        )
        self.output = output
        self.parse_info = []

    def _verbose_generate_config(self, generate_config):
        """"""
        if self.verbose:
            self._logger(msg="Generate Config: ", color='green')
            for key, val in generate_config.model_dump().items():
                if key != "messages":
                    self._logger(msg=f"{key}: {val}", color='cyan')
            self._logger(msg="\nMessages: ", color='blue')
            for message in generate_config.messages:
                self._logger(msg=f"{message.role}: {message.content[:10]} ...", color='cyan')

    def generate_stream(
            self,
            data: LLMRequest,
    ) -> Union[Iterable[Completion], Iterable[Message], Iterable[str]]:
        """"""
        _iters = invoke_sse_llm(url=self.model_name, data=data)
        for _iter in _iters:
            yield self._output(_iter)

    def generate_message(
            self,
            data: LLMRequest,
    ) -> Union[Completion]:
        """"""
        completion = invoke_llm(url=self.model_name, data=data)
        return completion

    def generate_prepare(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ):
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.llm_request.messages = messages
        self.generate_config.messages = messages
        self._verbose_generate_config(generate_config=self.generate_config)

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[Completion, CompletionMessage, Iterable[Completion], str]:
        """"""
        self.generate_prepare(query=query, messages=messages)
        if self.generate_config.stream:
            return self.generate_stream(data=self.llm_request)
        else:
            completion = self.generate_message(data=self.llm_request)
            return self._output(completion)

    def generate_with_parse(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            parse_fun: Optional[Callable] = None,
            parse_dict: Literal["eval", "greedy", "nested"] = "eval",
    ) -> Union[List[Any], List[List], List[Dict], str]:
        """

        :param parse_dict:
        :param query:
        :param messages:
        :param parse_fun:
        :return:
        """
        self.generate_prepare(query=query, messages=messages)
        completion = self.generate_message(data=self.llm_request)
        content = completion.choices[0].message.content
        try:
            parsed_data = self._parse_out(content=content, parse_fun=parse_fun, parse_dict=parse_dict)
            self.parse_info.append(ParseInfo(content=content, parsed_data=parsed_data))
            return parsed_data
        except Exception as error:
            self.parse_info.append(ParseInfo(content=content, error_message=error))
            return content
