from pandas import DataFrame
from typing import List, Union, Optional, Literal
from pydantic import ConfigDict, Field
from .base import Message
from .content import TextContent, TableContent


__all__ = ['TableMessage']


class TableMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user", "assistant"] = Field(
        default="user",
        description="""The role of the author of this message.""")
    content: Optional[Union[str, List[Union[TextContent, TableContent]]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(self, tables: Optional[List[DataFrame]] = None, **kwargs):
        super().__init__(**kwargs)
        _content = []
        if isinstance(self.content, list):
            _content = self.content
        elif isinstance(self.content, str):
            _content.append(self._add_content(self.content))
        if isinstance(tables, list):
                for table in tables:
                    _content.append(self._add_table(table))
        self.content = _content

    def _add_content(self, content: str) -> TextContent:
        """"""
        return TextContent(text=content)

    def _add_table(self, table: str) -> TableContent:
        """"""
        return TableContent(table=table)

    def show_streamlit(self):
        st = self._validate_streamlit()
        if isinstance(self.content, str):
            st.markdown(self.content)
        if isinstance(self.content, list):
            for _content in self.content:
                if isinstance(_content, TextContent):
                    st.markdown(_content.text)
                if isinstance(_content, TableContent):
                    st.dataframe(_content.table)
