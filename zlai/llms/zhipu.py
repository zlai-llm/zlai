try:
    from zhipuai import ZhipuAI
except ModuleNotFoundError:
    print(ModuleNotFoundError("pip install zhipuai"))

import os
import time
from typing import Any, List, Dict, Literal, Callable, Optional, Iterable
from zlai.types.chat import ChatCompletion, ChatCompletionChunk
from ..schema import *
from .generate import Generate
from .generate_config import TypeZhipuGenerate, GLM4FlashGenerateConfig


__all__ = ["Zhipu"]


def get_unknown_async_completion(resp: AsyncTaskStatus) -> AsyncCompletion:
    """"""
    choice = CompletionChoice(
        index=0,
        finish_reason='unknown',
        message=CompletionMessage(
            role='assistant',
        ),
    )
    usage = CompletionUsage(
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
    )
    async_completion = AsyncCompletion(
        id=resp.id,
        request_id=resp.request_id,
        model=resp.model,
        task_status=resp.task_status,
        choices=[choice],
        usage=usage,
    )
    return async_completion


class Zhipu(Generate):
    """"""
    api_key: Optional[str]
    api_key_name: Optional[str]
    model_name: Optional[str]
    generate_config: Optional[TypeZhipuGenerate]
    messages: List[Message]
    parse_info: List[ParseInfo]
    async_task_response: Optional[List]
    zhipu_client: Optional[ZhipuAI]
    async_max_request_time: Optional[int] = 600

    def __init__(
            self,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            generate_config: Optional[TypeZhipuGenerate] = GLM4FlashGenerateConfig(),
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = "ZHIPU_API_KEY",
            async_max_request_time: Optional[int] = 600,
    ):
        """"""
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.messages = messages
        self.generate_config = generate_config
        self.model_name = generate_config.model
        self.async_max_request_time = async_max_request_time
        self.verbose = verbose
        self.output = output
        self.parse_info = []
        self._create_client()

    def _create_client(self):
        """"""
        if self.api_key:
            self.zhipu_client = ZhipuAI(api_key=self.api_key)
        elif os.getenv(self.api_key_name):
            self.api_key = os.getenv(self.api_key_name)
            self.zhipu_client = ZhipuAI(api_key=self.api_key)
        else:
            raise ValueError(f"api_key not found, please set api key")

    def generate_stream(
            self,
            response: Iterable[ChatCompletionChunk],
    ) -> Union[Iterable[ChatCompletionChunk], Iterable[Message], Iterable[str]]:
        """"""
        for chunk in response:
            yield self._output(chunk)

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[ChatCompletion, CompletionMessage, Iterable[ChatCompletionChunk], str]:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = messages
        completion = self.zhipu_client.chat.completions.create(**self.generate_config.model_dump())

        if self.generate_config.stream:
            # completion = ChatCompletionChunk.model_validate(completion.model_dump())
            return self.generate_stream(completion)
        else:
            completion = ChatCompletion.model_validate(completion.model_dump())
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

        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = messages
        completion = self.zhipu_client.chat.completions.create(**self.generate_config.model_dump())
        content = completion.choices[0].message.content
        try:
            parsed_data = self._parse_out(content=content, parse_fun=parse_fun, parse_dict=parse_dict)
            self.parse_info.append(ParseInfo(content=content, parsed_data=parsed_data))
            return parsed_data
        except Exception as error:
            self.parse_info.append(ParseInfo(content=content, error_message=error))
            return content

    def async_generate_zhipu(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> AsyncTaskStatus:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = messages
        generate_config = self.generate_config.model_dump()
        generate_config.pop("stream")
        response = self.zhipu_client.chat.asyncCompletions.create(**generate_config)
        return response

    def async_generate(
            self,
            query_list: Optional[List[str]] = None,
            messages_list: Optional[List[List[Message]]] = None,
    ) -> Union[List[CompletionMessage], List[AsyncCompletion]]:
        """"""
        if messages_list:
            pass
        elif query_list:
            messages_list = [self._make_messages(query=query) for query in query_list]
        else:
            raise ValueError("Either query_list or messages_list should be provided")
        self.async_task_response = []
        for messages in messages_list:
            resp = self.async_generate_zhipu(messages=messages)
            self.async_task_response.append(resp)
        completions = list(map(self.get_retrieve_completion, self.async_task_response))
        return completions

    def async_generate_with_parse(
            self,
            query_list: Optional[List[str]] = None,
            messages_list: Optional[List[List[Message]]] = None,
            parse_fun: Optional[Callable] = None,
            parse_dict: Literal["eval", "greedy", "nested"] = "eval",
    ) -> Union[List[Any], List[List], List[Dict], str]:
        """"""
        if self.generate_config.stream:
            raise ValueError("Stream mode not support parse.")
        completions = self.async_generate(query_list=query_list, messages_list=messages_list)
        contents = [completion.choices[0].message.content for completion in completions]

        parsed_contents = []
        for content in contents:
            try:
                parsed_data = self._parse_out(content=content, parse_fun=parse_fun, parse_dict=parse_dict)
                self.parse_info.append(ParseInfo(content=content, parsed_data=parsed_data))
                parsed_contents.append(parsed_data)
            except Exception as error:
                self.parse_info.append(ParseInfo(content=content, error_message=error))
                parsed_contents.append(content)
        return parsed_contents

    def get_retrieve_completion(
            self,
            resp: AsyncTaskStatus,
            sleep: int = 1,
    ) -> AsyncCompletion:
        """"""
        task_id = resp.id
        task_status = ''
        cnt = 0
        while task_status != 'SUCCESS' and task_status != 'FAILED' and cnt <= self.async_max_request_time:
            response = self.zhipu_client.chat.asyncCompletions.retrieve_completion_result(
                id=task_id)
            task_status = response.task_status
            if task_status == 'SUCCESS':
                return response
            else:
                time.sleep(sleep)
                cnt += 1
        return get_unknown_async_completion(resp)
