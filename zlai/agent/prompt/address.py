from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from typing import List, ClassVar
from ...schema.messages import Message, SystemMessage, UserMessage, AssistantMessage
from ...prompt import MessagesPrompt


__all__ = [
    "PromptTemplate",
    "PromptAddress",
]


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


@dataclass
class PromptAddress:
    """"""
    # address
    system_message: SystemMessage = system_message
    few_shot: ClassVar[List[Message]] = few_shot
    messages_prompt: MessagesPrompt = MessagesPrompt(
        system_message=system_message,
        few_shot=few_shot,
        n_shot=5,
    )

