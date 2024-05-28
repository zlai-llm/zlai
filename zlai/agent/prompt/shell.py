from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from ...schema.messages import Message, SystemMessage


__all__ = [
    "PromptShell",
]


system_message = SystemMessage(content="You are a helpful SHELL assistant.")


@dataclass
class PromptShell:
    """"""
    system_message: SystemMessage = system_message

