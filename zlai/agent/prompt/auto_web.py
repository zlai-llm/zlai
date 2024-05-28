from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from ...schema.messages import SystemMessage


__all__ = [
    "PromptTemplate",
    "PromptAutoWeb",
]


system_message = SystemMessage(
    content="""You were a helpful assistant, answering questions using the reference content provided.""")
PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""
summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY_TMP)


@dataclass
class PromptAutoWeb:
    """"""
    # address
    system_message: SystemMessage = system_message
    summary_prompt: PromptTemplate = summary_prompt

