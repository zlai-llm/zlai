import streamlit as st
from pandas import DataFrame
from typing import List, Union
from zlai.types.messages.content import TextContent
from zlai.types.function_call import ChatCompletionMessageToolCall


__all__ = [
    "show_tool_call",
    "show_observation",
]


def show_tool_call(tool_call: ChatCompletionMessageToolCall):
    """"""
    arguments = tool_call.function.arguments
    try:
        arguments = eval(arguments)
    except:
        pass

    with st.expander(f"Tool Call: {tool_call.function.name}"):
        if isinstance(arguments, dict):
            st.json(arguments)
        else:
            st.write(arguments)


def show_observation(content: Union[str, List[TextContent]]):
    """"""
    try:
        _content = eval(content)
    except:
        _content = content

    with st.expander("Observation"):
        if isinstance(_content, DataFrame):
            st.table(_content)
        elif isinstance(_content, (list, dict)):
            st.json(_content)
        else:
            st.markdown(_content)
