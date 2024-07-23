from pydantic import BaseModel
from typing import Any, List, Literal, Optional
from ..schema import Message


__all__ = [
    "PromptTemplate",
    "StringPromptValue",
]


class StringPromptValue(BaseModel):
    text: str

    def to_string(self) -> str:
        """Return prompt as string."""
        return self.text

    def to_messages(
            self,
            role: Literal["system", "user", "assistant"],
    ) -> Message:
        """Return prompt as messages."""
        return Message(role=role, content=self.text)


class PromptTemplate(BaseModel):
    """"""
    text: Optional[str] = None
    input_variables: Optional[List[str]] = None
    template: Optional[str] = None

    def __init__(
            self,
            input_variables: list[str],
            template: str,
            **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.input_variables = input_variables
        self.template = template

    def format(self, **kwargs) -> StringPromptValue:
        self.text = self.template.format(**kwargs)
        return StringPromptValue(text=self.text)

    def format_prompt(self, **kwargs: Any) -> StringPromptValue:
        self.text = self.template.format(**kwargs)
        return StringPromptValue(text=self.text)
