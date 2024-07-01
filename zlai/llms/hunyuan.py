try:
    from tencentcloud.common.credential import Credential
    from tencentcloud.hunyuan.v20230901.models import ChatCompletionsRequest
    from tencentcloud.hunyuan.v20230901.hunyuan_client import HunyuanClient
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install --upgrade tencentcloud-sdk-python")

import os
import json
from typing import List, Dict, Literal, Optional, Iterable, Callable

from ..schema import *
from .generate import Generate
from .generate_config.hunyuan import TypeHunYuanGenerate


__all__ = ["HunYuan"]


def to_camel_case(string: str) -> str:
    """"""
    words = string.split('_')
    camel_case = words[0].capitalize()
    for word in words[1:]:
        camel_case += word.capitalize()
    return camel_case


def to_snake_case(string: str) -> str:
    """"""
    upper_indices = [i for i, char in enumerate(string) if char.isupper()]
    string_lower = string.lower()
    segments = []
    start = 0
    for index in upper_indices:
        segments.append(string_lower[start: index])
        start = index
    segments.append(string_lower[start:])
    segments = [segment for segment in segments if segment]
    return "_".join(segments)


def trans_dict_keys_format(d: Dict, trans_fun: Optional[Callable] = to_camel_case):
    """"""
    new_d = {}
    for key, value in d.items():
        if isinstance(value, dict):
            new_d[trans_fun(key)] = trans_dict_keys_format(value, trans_fun=trans_fun)
        elif isinstance(value, list):
            new_d[trans_fun(key)] = [trans_dict_keys_format(item, trans_fun=trans_fun) if isinstance(item, dict) else item for item in value]
        else:
            new_d[trans_fun(key)] = value
    return new_d


class HunYuan(Generate):
    """"""
    api_key: Optional[str]
    api_key_name: Optional[str]
    generate_config: TypeHunYuanGenerate
    messages: List[Message]
    parse_info: List[ParseInfo]
    async_task_response: Optional[List]
    client: Optional[HunyuanClient]
    async_max_request_time: Optional[int] = 600

    def __init__(
            self,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            generate_config: Optional[TypeHunYuanGenerate] = None,
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "HUNYUAN_API_KEY",
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
            pass
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
        else:
            raise ValueError(f"api_key not found, please set api key")
        secret_id, secret_key = self.api_key.split(":")
        self.client = HunyuanClient(
            Credential(secret_id=secret_id, secret_key=secret_key), region="ap-beijing")

    def _make_request(self, generate_config: TypeHunYuanGenerate) -> HunyuanClient.ChatCompletions:
        """"""
        request = ChatCompletionsRequest()
        param = trans_dict_keys_format(generate_config.model_dump(), trans_fun=to_camel_case)
        request.from_json_string(json.dumps(param))
        response = self.client.ChatCompletions(request)
        return response

    def _trans_choice(self, chunk: Dict) -> List[CompletionChoice]:
        """"""
        choices = chunk.get("choices")
        _ = [choice.update({"index": i, "message": choice.get("delta")}) for i, choice in enumerate(choices)]
        choices = [CompletionChoice.model_validate(choice) for choice in choices]
        return choices

    def generate_stream(
            self,
            response: Iterable[Dict],
    ) -> Union[Iterable[Completion], Iterable[Message], Iterable[str]]:
        """"""
        for chunk in response:
            chunk = eval(chunk.get("data"))
            chunk = trans_dict_keys_format(chunk, trans_fun=to_snake_case)
            chunk = Completion(
                model=self.generate_config.model,
                created=chunk.get("created"),
                choices=self._trans_choice(chunk),
                request_id=chunk.get("id"),
                id=chunk.get("id"),
                usage=CompletionUsage.model_validate(chunk.get("usage")),
            )

            chunk = Completion.model_validate(chunk)
            yield self._output(chunk)

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[Completion, CompletionMessage, Iterable[Completion], str]:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = messages
        response = self._make_request(self.generate_config)

        if self.generate_config.stream:
            return self.generate_stream(response)
        else:
            response = trans_dict_keys_format(json.loads(response.to_json_string()), trans_fun=to_snake_case)
            completion = Completion.model_validate(response)
            return self._output(completion)
