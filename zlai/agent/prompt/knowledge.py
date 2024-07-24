from ...schema.messages import SystemMessage
from ...prompt import PromptTemplate
from ..schema import AgentPrompt


__all__ = [
    "PROMPT_SUMMARY",
    "system_message",
    "summary_prompt",
    "prompt_knowledge",
]


PROMPT_SUMMARY = """
参考文本:{content}

参考上面的文本，依据文本内容总结回答用户的问题:{question}"""

system_message = SystemMessage(content="You are a helpful assistant. \
You have to answer questions according to the reference text provided")

summary_prompt = PromptTemplate(
    input_variables=["content", "question"],
    template=PROMPT_SUMMARY)

prompt_knowledge = AgentPrompt(system_message=system_message, prompt_template=summary_prompt)
