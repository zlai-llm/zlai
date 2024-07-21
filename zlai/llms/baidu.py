# https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2
# 【推荐】使用安全认证AK/SK鉴权，通过环境变量初始化认证信息,
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
# os.environ["QIANFAN_ACCESS_KEY"] = "your_iam_ak"
# os.environ["QIANFAN_SECRET_KEY"] = "your_iam_sk"

try:
    from qianfan import ChatCompletion
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install qianfan")

from typing import List, Dict, Literal, Optional, Iterable
from ..schema import *
from .generate import Generate
from .generate_config.baidu import TypeBaiduGenerate, ErnieTiny8KGenerateConfig


__all__ = [
    "Baidu",
]


class Baidu(Generate):
    """"""
    api_key: Optional[str]
    api_key_name: Optional[str]
    model_name: Optional[str]
    generate_config: TypeBaiduGenerate
    messages: List[Message]

    def __init__(
            self,
            api_key: Optional[str] = None,
            messages: Optional[List[Message]] = None,
            generate_config: TypeBaiduGenerate = ErnieTiny8KGenerateConfig(),
            output: Literal["completion", "message", "str"] = "completion",
            verbose: Optional[bool] = False,
            api_key_name: Optional[str] = None,
    ):
        """"""
        self.api_key = api_key
        self.api_key_name = api_key_name
        self.messages = messages
        self.generate_config = generate_config
        self.model_name = generate_config.model
        self.verbose = verbose
        self.output = output
        self._create_client()

    def _create_client(self):
        self.baidu_client = ChatCompletion()

    def _make_baidu_completion(self, body: Dict) -> Completion:
        """"""
        message = CompletionMessage(content=body.get("result"), role="assistant")
        completion = Completion(
            model=self.generate_config.model,
            created=body.get("created"),
            choices=[CompletionChoice(index=0, finish_reason="stop", message=message)],
            request_id=body.get("id"),
            id=body.get("id"),
            usage=CompletionUsage.model_validate(body.get("usage")),
        )
        return completion

    def generate_stream(
            self,
            response: Iterable[Dict],
    ) -> Union[Iterable[Completion], Iterable[Message], Iterable[str]]:
        """"""
        for chunk in response:
            body = chunk["body"]
            completion = self._make_baidu_completion(body)
            yield self._output(completion)

    def generate(
            self,
            query: Optional[str] = None,
            messages: Optional[List[Message]] = None,
    ) -> Union[Completion, CompletionMessage, Iterable[Completion], str]:
        """"""
        messages = self._make_messages(query=query, messages=messages)
        self.generate_config.messages = messages
        response = self.baidu_client.do(**self.generate_config.model_dump())
        if self.generate_config.stream:
            return self.generate_stream(response)
        else:
            body = response["body"]
            completion = self._make_baidu_completion(body)
            return self._output(completion)
