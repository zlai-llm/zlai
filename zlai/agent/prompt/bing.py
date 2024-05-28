from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from ...schema import SystemMessage

__all__ = [
    "PromptTemplate",
    "summary_prompt",
    "system_message",
    "PromptBingSearch",
]

PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""

summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY_TMP)

system_message = SystemMessage(
    content="""You were a helpful assistant, answering questions using the reference content provided.""")


@dataclass
class PromptBingSearch:
    """"""
    system_message: SystemMessage = system_message
    summary_prompt: PromptTemplate = summary_prompt
