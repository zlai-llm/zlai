from langchain.prompts import PromptTemplate
from ..schema import SystemMessage

__all__ = [
    "summary_prompt",
    "system_message",
]

PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""

summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY_TMP)

system_message = SystemMessage(
    content="""You were a helpful assistant, answering questions using the reference content provided.""")

