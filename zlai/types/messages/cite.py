from typing import List, Union, Literal, Optional, Dict
from pydantic import ConfigDict, Field
from .base import Message
from .content import QueryContent, CiteContent


__all__ = [
    "CiteMessage",
]


class CiteMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user", "assistant"] = Field(default="user", description="""The role of the author of this message.""")
    content: Optional[List[Union[QueryContent, CiteContent]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(self, query: Optional[str] = None, cite: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.content, list):
            _content = self.content
        else:
            _content = []
            if query:
                _content.append(QueryContent(content=query))
            if cite:
                _content.append(CiteContent(content=cite))
        self.content = _content

    def to_message(self):
        """"""
        return self

    def to_dict(self) -> Dict:
        """"""
        return self.model_dump()

    def show_streamlit(self) -> None:
        """"""
        st = self._validate_streamlit()
        if isinstance(self.content, list):
            for item in self.content:
                if isinstance(item, QueryContent):
                    st.markdown(item.content)
                elif isinstance(item, CiteContent):
                    with st.expander(f"Cite: "):
                        st.markdown(item.content)
        else:
            st.markdown(self.content)
