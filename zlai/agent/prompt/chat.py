from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from typing import List, ClassVar, Optional
from ...schema.messages import Message, SystemMessage
from ...prompt import MessagesPrompt


__all__ = [
    "PromptTemplate",
    "PromptChat",
]


system_message = SystemMessage(content="""You are a helpful assistant.""")


@dataclass
class PromptChat:
    """"""
    # address
    system_message: SystemMessage = system_message
    few_shot: ClassVar[List[Message]] = []
    messages_prompt: Optional[MessagesPrompt] = None
    prompt_template: Optional[PromptTemplate] = None
