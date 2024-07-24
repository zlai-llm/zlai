from ...prompt import PromptTemplate
from ...schema import SystemMessage
from ..schema import AgentPrompt

__all__ = [
    "summary_prompt",
    "system_message",
    "prompt_bing_search",
]

PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""

summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY_TMP)

system_message = SystemMessage(
    content="""You were a helpful assistant, answering questions using the reference content provided.""")

prompt_bing_search = AgentPrompt(system_message=system_message, prompt_template=summary_prompt)
