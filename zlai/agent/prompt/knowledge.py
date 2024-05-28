from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from typing import Optional
from ...schema.messages import SystemMessage


__all__ = [
    "PromptTemplate",
    "PROMPT_SUMMARY",
    "system_message",
    "summary_prompt",
    "PromptKnowledge",
]


PROMPT_SUMMARY = """
参考文本:{content}

参考上面的文本，依据文本内容总结回答用户的问题:{question}"""

system_message = SystemMessage(content="You are a helpful assistant. \
You have to answer questions according to the reference text provided")

summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY)


@dataclass
class PromptKnowledge:
    """"""
    system_message: SystemMessage = system_message
    summary_prompt: Optional[PromptTemplate] = summary_prompt
