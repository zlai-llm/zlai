from ...prompt import PromptTemplate
from ...schema.messages import SystemMessage
from ..schema import AgentPrompt


__all__ = [
    "prompt_auto_web",
]


system_message = SystemMessage(
    content="""You were a helpful assistant, answering questions using the reference content provided.""")
PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""
summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY_TMP)

prompt_auto_web = AgentPrompt(system_message=system_message, prompt_template=summary_prompt)
