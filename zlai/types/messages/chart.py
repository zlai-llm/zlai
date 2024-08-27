import re
import warnings
from typing import List, Union, Tuple, Literal, Optional
from pydantic import ConfigDict, Field
from bs4 import BeautifulSoup
from .base import Message
from .content import TextContent, ChartContent


__all__ = [
    "ChartMessage",
]


class ChartMessage(Message):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    role: Literal["user", "assistant"] = Field(
        default="user",
        description="""The role of the author of this message.""")
    content: Optional[Union[str, List[Union[TextContent, ChartContent]]]] = Field(
        default=None, description="""The content of the message.""")

    def __init__(self, charts: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        _content = []
        if isinstance(self.content, list):
            _content = self.content
        elif isinstance(self.content, str):
            _content.append(self._add_content(self.content))
        if isinstance(charts, list):
            for chart in charts:
                _content.append(self._add_chart(chart))
        self.content = _content

    def _add_content(self, content: str) -> TextContent:
        """"""
        return TextContent(text=content)

    def _add_chart(self, chart: str) -> ChartContent:
        """"""
        return ChartContent(chart=chart)

    def _chart_size(self, chart: str) -> Tuple[int, int]:
        """"""
        soup = BeautifulSoup(chart, features='html.parser')
        chart_container = soup.find(name='div', attrs={'class': 'chart-container'})
        width, height = re.findall(r'\d+', chart_container.get('style'))
        width, height = int(width), int(height)

        if width > 640:
            message = f"width of chart is too large: {width}, adjusting to 640px."
            warnings.warn(message)
        return width, height

    def show_streamlit(self):
        st = self._validate_streamlit()
        import streamlit.components.v1 as components
        if isinstance(self.content, str):
            st.markdown(self.content)
        if isinstance(self.content, list):
            for _content in self.content:
                if isinstance(_content, TextContent):
                    st.markdown(_content.text)
                if isinstance(_content, ChartContent):
                    width, height = self._chart_size(chart=_content.chart)
                    components.html(_content.chart, scrolling=True, width=width, height=height)
