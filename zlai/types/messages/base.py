from pydantic import BaseModel, Field


__all__ = [
    "Message"
]


class Message(BaseModel):
    """"""
    role: str = Field(default="", description="角色")
    content: str = Field(default="", description="对话内容")

    def _validate_streamlit(self):
        """"""
        try:
            import streamlit as st
            return st
        except ImportError:
            raise ImportError("Please install streamlit to use this function, < pip install streamlit >")

    def to_message(self):
        """"""
        return self.model_dump()

    def show_streamlit(self):
        """"""
        st = self._validate_streamlit()
        if isinstance(self.content, str):
            st.markdown(self.content)
