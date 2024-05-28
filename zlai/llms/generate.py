try:
    from openai import OpenAI
    from openai.types.chat import ChatCompletion, ChatCompletionChunk
    from openai._streaming import Stream
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install openai")

import os
from typing import Any, Union, List, Dict, Iterable, Literal, Optional, Callable
from ..schema import *
from ..utils import *
from ..parse import *


__all__ = [
    "Generate",
    "OpenAICompletion",
]


class Generate(LoggerMixin):
    """"""
    output: Literal["completion", "message", "str"] = "completion"

    @classmethod
    def _make_messages(
            cls,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> List[Message]:
        """"""
        if messages:
            messages = messages
        elif query:
            messages = [Message(role="user", content=query)]
        return messages

    def _output(
            self,
            completion: Completion
    ) -> Union[Completion, CompletionMessage, str]:
        """"""
        if self.output == "completion":
            return completion
        elif self.output == "message":
            return completion.choices[0].message
        elif self.output == "str":
            return completion.choices[0].message.content
        else:
            raise ValueError(f"Unsupported output type: {self.output}")

    @classmethod
    def _parse_out(
            cls,
            content: str,
            parse_fun: Optional[Callable] = None,
            parse_dict: Literal["eval", "greedy", "nested"] = "eval",
    ):
        """"""
        parse = ParseString()
        if parse_fun:
            try:
                return parse_fun(content)
            except Exception as e:
                raise AttributeError(f"parse_fun error: {e}")
        elif parse_dict == "eval":
            return parse.eval_dict(string=content)
        elif parse_dict == "greedy":
            return parse.eval_dict(string=content)
        elif parse_dict == "nested":
            return parse.eval_dict(string=content)
        else:
            raise ValueError(f"Unsupported parse: {parse_dict}.")


class OpenAICompletion(Generate):
    """Atom 模型不支持异步调用"""
    api_key: Optional[str]
    api_key_name: Optional[str]
    generate_config: Optional[GenerateConfig]
    messages: List[Message]
    parse_info: List[ParseInfo]
    api_key_name: Optional[str]
    verbose: Optional[bool]
    base_url: Optional[str]
    output: Literal["completion", "message", "str"] = "completion"

    def __init__(
            self,
            generate_config: Optional[GenerateConfig],
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = None,
            *args: Any,
            **kwargs: Any,
    ):
        """"""
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.messages = messages
        self.generate_config = generate_config
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self.args = args
        self.kwargs = kwargs

    def _create_client(self):
        """"""
        if self.api_key:
            pass
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
        else:
            raise ValueError(f"api_key not found, please set api key")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _output(
            self,
            response: Union[ChatCompletionChunk, ChatCompletion],
    ) -> Union[ChatCompletion, Message, str]:
        """"""
        if self.output == "completion":
            return response
        elif self.output == "message":
            message = AssistantMessage.model_validate(response.choices[0].delta.model_dump())
            return message
        elif self.output == "str":
            return response.choices[0].delta.content
        else:
            raise ValueError(f"Unsupported output type: {self.output}")

    def generate_stream(
            self,
            completions: Union[Iterable[ChatCompletion], Stream[ChatCompletionChunk]],
    ) -> Union[Iterable[ChatCompletion], Iterable[Message], Iterable[str]]:
        """"""
        for completion in completions:
            yield self._output(completion)

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[ChatCompletion, Message, Iterable[ChatCompletion], str]:
        """"""
        self.generate_config.messages = self._make_messages(query=query, messages=messages)
        completion = self.client.chat.completions.create(**self.generate_config.model_dump())
        if self.generate_config.stream:
            return self.generate_stream(completion)
        else:
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
