import json
import requests
from typing import List, Union, Iterable
from ..schema import *
from ..schema.response import *


__all__ = [
    "llm_url",
    "invoke_llm",
    "invoke_sse_llm",
    "validate_messages",

    "completion_message",
    "completion_content",
    "get_unknown_completion_message",
    "get_unknown_async_completion",
]

headers = {'Content-Type': 'application/json'}
llm_url = LLMUrl


def completion_message(completion: Completion) -> Union[CompletionMessage, Message]:
    """"""
    return completion.choices[0].message


def completion_content(completion: Completion) -> str:
    """"""
    return completion.choices[0].message.content


def get_unknown_completion_message() -> CompletionMessage:
    """"""
    message = CompletionMessage(
        role='assistant',
    )
    return message


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


def validate_messages(
        messages: Union[List[Message], List[CompletionMessage]]
) -> ValidateMessagesResponded:
    """
    todo: 验证其他类型的 Message.
    对于输入消息的验证
    :param messages:
    :return:
    """
    responded = ValidateMessagesResponded()

    if messages[-1].role != Role.user:
        responded.message = f"Last message role must be {Role.user}."
        responded.access = False
        return responded

    for i, message in enumerate(messages):
        if i != 0 and message.role == Role.system:
            responded.message = f"System message id {i} is not allowed."
            responded.access = False
            return responded
        else:
            pass
    return responded


def invoke_llm(
        url: Union[LLMUrl, str],
        data: LLMRequest,
        timeout: int = 600,
) -> Completion:
    """

    :param url:
    :param data:
    :param timeout:
    :return:
    """
    validate_info = validate_messages(data.messages)
    try:
        response = requests.post(url, data=json.dumps(data.model_dump()), headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"RequestException: {e}")

    if validate_info.access:
        completion = Completion.model_validate(response.json())
        return completion
    else:
        raise TypeError(f"ERROR: {validate_info.message}")


def invoke_sse_llm(
        url: Union[LLMUrl, str],
        data: LLMRequest,
        timeout: int = 600,
) -> Iterable[Completion]:
    """

    :param url:
    :param data:
    :param timeout:
    :return:
    """
    validate_info = validate_messages(data.messages)

    if validate_info.access:
        try:
            response = requests.post(url, data=json.dumps(data.model_dump()), stream=True, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"RequestException: {e}")

        for item in response.iter_lines():
            text = json.loads(item)
            completion = Completion.model_validate(text)
            for choice in completion.choices:
                choice.message.content = choice.message.content.replace("<|n|>", "\n")
            yield completion
    else:
        raise TypeError(f"ERROR: {validate_info.message}")
