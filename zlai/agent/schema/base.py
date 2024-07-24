from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from zlai.prompt import MessagesPrompt, PromptTemplate
from zlai.schema import Message, SystemMessage


__all__ = [
    "AgentPrompt",
]


class AgentPrompt(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    system_message: Optional[SystemMessage] = Field(default=None, description="")
    system_template: Optional[PromptTemplate] = Field(default=None, description="")
    few_shot: Optional[List[Message]] = Field(default=None, description="")
    messages_prompt: Optional[MessagesPrompt] = Field(default=None, description="")
    prompt_template: Optional[PromptTemplate] = Field(default=None, description="")
