try:
    import dashscope
    from dashscope import Generation
    from dashscope.aigc.generation import GenerationResponse, Message as AliMessage
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install dashscope")

import os
import time
from typing import (
    Any, List, Union, Dict, Literal,
    Callable, Optional, Iterable)
from http import HTTPStatus

from ..schema import *
from .base import *
from .generate import Generate
from .generate_config import *


__all__ = ["Ali"]


class Ali(Generate):
    """阿里模型不支持异步调用"""
    api_key: Optional[str]
    api_key_name: Optional[str]
    generate_config: TypeAliGenerate
    messages: List[Message]
    parse_info: List[ParseInfo]
    output: Literal["response", "message", "str"] = "response"

    def __init__(
            self,
            generate_config: TypeAliGenerate,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["response", "message", "str"] = "response",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "ALI_API_KEY",
    ):
        """"""
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.messages = messages
        self.generate_config = generate_config
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self._create_client()

    def _create_client(self):
        """"""
        if self.api_key:
            dashscope.api_key = self.api_key
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
            dashscope.api_key = self.api_key
        else:
            raise ValueError(f"api_key not found, please set api key")

    def _output(
            self,
            response: GenerationResponse,
    ) -> Union[GenerationResponse, AliMessage, str]:
        """"""
        if self.output == "response":
            return response
        elif self.output == "message":
            return response.choices[0].message
        elif self.output == "str":
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unsupported output type: {self.output}")

    def trans_zhipu_completion(self, response: GenerationResponse) -> Completion:
        """"""
        message = Message(
            role=response.output.choices[0].message.role,
            content=response.output.choices[0].message.content,
        )
        completion_choice = CompletionChoice(
            finish_reason=response.output.choices[0].finish_reason,
            message=message,
        )
        usage = CompletionUsage(
            completion_tokens=response.usage.input_tokens,
            total_tokens=response.usage.output_tokens + response.usage.input_tokens,
        )
        completion = Completion(
            model=self.generate_config.model,
            choices=[completion_choice],
            usage=usage,
        )
        return completion

    def error_completion(self, ):
        """"""
        return None

    def generate_stream(
            self,
            responses: Iterable[GenerationResponse],
    ) -> Union[Iterable[GenerationResponse], Iterable[AliMessage], Iterable[str]]:
        """"""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                yield self._output(response)
            else:
                msg = f'Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}'
                self._logger(msg=msg)
                self._logger(msg=f"Messages: {self.generate_config.messages.model_dump()}")

    def generate_message(
            self,
            response: GenerationResponse,
    ) -> Union[GenerationResponse, AliMessage, str]:
        """"""
        if response.status_code == HTTPStatus.OK:
            return self._output(response)
        else:
            msg = f'Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}'
            self._logger(msg=msg)
            self._logger(msg=f"Messages: {self.generate_config.messages.model_dump()}")

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[GenerationResponse, AliMessage, Iterable[GenerationResponse], str]:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = [message.model_dump() for message in messages]

        response = dashscope.Generation.call(**self.generate_config.model_dump())
        if self.generate_config.stream:
            return self.generate_stream(response)
        else:
            return self.generate_message(response)

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
        if self.generate_config.stream:
            raise ValueError("Stream mode not support parse.")
        response = self.generate(query=query, messages=messages)
        content = response.output.choices[0].message.content
        try:
            parsed_data = self._parse_out(content=content, parse_fun=parse_fun, parse_dict=parse_dict)
            self.parse_info.append(ParseInfo(content=content, parsed_data=parsed_data))
            return parsed_data
        except Exception as error:
            self.parse_info.append(ParseInfo(content=content, error_message=error))
            return content


# class AliVL(Generate):
#     """"""
#     def __init__(self):
#         """"""
#
#     def generate(self):
#         """"""
#         response = dashscope.MultiModalConversation.call(
#             model=self.model_name,
#             messages=messages,
#             **self.generate_config,
#         )
