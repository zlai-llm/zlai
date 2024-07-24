import unittest
from pydantic import BaseModel, Field, ConfigDict
from typing import ClassVar, List, Optional
from zlai.schema import *
from zlai.prompt import *


system_message = SystemMessage(content="""你是一个地址命名实体识别机器人，你需要解析出文本中出现的省、市、区，并以Dict输出。\
文本中没有省、市、区，则返回空Dict。""")

few_shot = [
    UserMessage(content="上海市浦东新区张江高科技园区"),
    AssistantMessage(content=str({'province': '上海市', 'city': '上海市', 'district': '浦东新区'})),
    UserMessage(content="广东省深圳市南山区深南大道1001号"),
    AssistantMessage(content=str({'province': '广东省', 'city': '深圳市', 'district': '南山区'})),
    UserMessage(content="河北省衡水市景县的天气情况"),
    AssistantMessage(content=str({'province': '河北省', 'city': '衡水市', 'district': '景县'})),
    UserMessage(content="你好呀"),
    AssistantMessage(content=str({})),
]


class PromptAddress(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    system_message: SystemMessage = Field(default=system_message, description="system message")
    few_shot: List[Message] = Field(default=few_shot, description="few shot examples")
    messages_prompt: MessagesPrompt = Field(
        default=MessagesPrompt(
            system_message=system_message,
            few_shot=few_shot,
            n_shot=5,)
    )


class TestTemp(unittest.TestCase):
    """"""
    def test_dataclass(self, ):
        """"""
        prompt = PromptAddress(
            system_message=system_message,
            few_shot=few_shot,
            messages_prompt=MessagesPrompt(
                system_message=system_message,
                few_shot=few_shot,
                n_shot=5,),
        )
        print(prompt.messages_prompt.few_shot)
        print(prompt.messages_prompt.prompt_format(content='text'))
        print(prompt)
