from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from zlai.prompt.base import MessagesPrompt
from zlai.prompt.template import PromptTemplate
from zlai.types.messages import TypeMessage, SystemMessage

__all__ = [
    "AgentPrompt",
]


class AgentPrompt(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    system_message: Optional[SystemMessage] = Field(default=None, description="")
    system_template: Optional[PromptTemplate] = Field(default=None, description="")
    few_shot: Optional[List[TypeMessage]] = Field(default=None, description="")
    messages_prompt: Optional[MessagesPrompt] = Field(default=None, description="")
    prompt_template: Optional[PromptTemplate] = Field(default=None, description="")

    def __init__(
            self,
            system_message: Optional[SystemMessage] = None,
            system_template: Optional[PromptTemplate] = None,
            few_shot: Optional[List[TypeMessage]] = None,
            messages_prompt: Optional[MessagesPrompt] = None,
            prompt_template: Optional[PromptTemplate] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.system_message = system_message
        self.system_template = system_template
        self.few_shot = few_shot
        self.messages_prompt = messages_prompt
        self.prompt_template = prompt_template
