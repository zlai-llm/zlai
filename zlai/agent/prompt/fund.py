from dataclasses import dataclass
from typing import List, ClassVar
from langchain.prompts import PromptTemplate

from ...prompt import MessagesPrompt
from ...schema.messages import Message, SystemMessage, UserMessage, AssistantMessage


__all__ = [
    "PromptTemplate",
    "PromptFund",
]


system_message = SystemMessage(content="""你是一个基金分析专家，需要你对基金相关领域问题给出专业回答，必要情况下会补充给你相关的数据，你需要依据真实数据进行如实回答。""")

# fund keyword info
system_message_fund_keyword = SystemMessage(content="""你是一个信息抽取机器人，你需要解析出问题中提到的基金名称或基金相关主题关键词，\
不需要关注问题的意图，只需要提取出基金名称或关键词，不要输出其他内容。""")

PromptFundKeyword = """你是一个信息抽取机器人，你需要解析出问题中提到的基金名称或基金相关主题关键词，\
不需要关注问题的意图，只需要提取出基金名称或关键词，不要输出其他内容。

问题: '{content}'
关键词: """

prompt_fund_keyword = PromptTemplate(
    input_variables=["content"],
    template=PromptFundKeyword)

few_shot_keyword = [
    UserMessage(content="""问题: '帮我找出新能源汽车相关基金'\n关键词: """),
    AssistantMessage(content="""新能源汽车"""),
    UserMessage(content="""问题: '帮我找出饲料相关基金'\n关键词: """),
    AssistantMessage(content="""饲料"""),
    UserMessage(content="""问题: '帮我找出豆粕相关基金'\n关键词: """),
    AssistantMessage(content="""豆粕"""),
    UserMessage(content="""问题: '查询有关于豆粕的基金代码'\n关键词: """),
    AssistantMessage(content="""豆粕"""),
    UserMessage(content="""问题: '查询有关于大成有色金属期货ETF联接A的基金代码'\n关键词: """),
    AssistantMessage(content="""大成有色金属期货ETF联接A"""),
]

# observation
PromptFundObservation = """Please answer the questions concisely according to the observation.

Observation: {observation}
Question: {question}
Answer: """

prompt_fund_observation = PromptTemplate(
    input_variables=["script", "observation", "question"],
    template=PromptFundObservation)

# extract fund code
system_message_fund_code = SystemMessage(
    content="""你需要判断并提取出问题中的基金编码，并直接输出编码，不需要输出其他内容。""")

few_shot_code = [
    UserMessage(content="""基金000001今天的行情怎么样？"""),
    AssistantMessage(content="""000001"""),
    UserMessage(content="""000011今天的行情怎么样？"""),
    AssistantMessage(content="""000011"""),
]

PromptFundCode = """你需要判断并提取出问题中的基金编码，并直接输出编码，不需要输出其他内容。

问题: '{content}'
code: """

prompt_fund_code = PromptTemplate(
    input_variables=["content"],
    template=PromptFundCode)

# fund code
PromptFindFundCode = """以下是依据给定的关键词`{keyword}`检索到的相关基金信息\

```
{code_info}
```

请简要介绍以上基金内容。"""

prompt_find_fund_code = PromptTemplate(
    input_variables=["keyword", "code_info"],
    template=PromptFindFundCode)

PromptFundDescription = """请根据以下基金基本信息回答问题。

基金基本信息：```{fund_description}```
问题：{question}"""

prompt_fund_description = PromptTemplate(
    input_variables=["fund_description", "question"],
    template=PromptFundDescription)

PromptFundStatus = """请根据以下基金净值信息回答问题。

基金基本信息：```{fund_status}```
问题：{question}"""

prompt_fund_status = PromptTemplate(
    input_variables=["fund_status", "question"],
    template=PromptFundStatus)


@dataclass
class PromptFund:
    """"""
    system_message: SystemMessage = system_message

    # fund keyword info
    system_message_fund_keyword: SystemMessage = system_message_fund_keyword
    few_shot_keyword: ClassVar[List[Message]] = few_shot_keyword
    prompt_fund_keyword: PromptTemplate = prompt_fund_keyword

    # fund observation
    prompt_fund_observation: PromptTemplate = prompt_fund_observation

    # extract fund code
    system_message_fund_code: SystemMessage = system_message_fund_code
    few_shot_code: ClassVar[List[Message]] = few_shot_code
    prompt_fund_code: PromptTemplate = prompt_fund_code

    # other
    prompt_find_fund_code: PromptTemplate = prompt_find_fund_code
    prompt_fund_description: PromptTemplate = prompt_fund_description
    prompt_fund_status: PromptTemplate = prompt_fund_status
