from typing import *
import pandas as pd
import streamlit as st
from dataclasses import dataclass, field
from streamlit.delta_generator import DeltaGenerator


__all__ = [
    "clear_chat_history",
    "Conversation",
    "append_conversation",
    "get_show_fun",
    "init_chat_history",
]


def clear_chat_history(st=st) -> None:
    """desc: 清除对话记录"""
    if st.session_state.get("messages"):
        del st.session_state.messages
    if st.session_state.get("show_messages"):
        del st.session_state.show_messages


def get_show_fun(placeholder: DeltaGenerator, display_type):
    """"""
    show_fun_dict = {
        "markdown": placeholder.markdown,
        "table": placeholder.table,
        "image": placeholder.image,
        "dataframe": placeholder.dataframe,
        "json": placeholder.json,
    }
    return show_fun_dict.get(display_type)


@dataclass
class Conversation:
    role: str
    content: Any
    tool: Union[str, None] = None
    display_type: str = 'markdown'
    display_info: Dict = field(default_factory=dict)

    def get_chat_prompt(self) -> Dict[str, str]:
        """"""
        chat_prompt = {
            "role": self.role,
            "content": self.content,
        }
        return chat_prompt

    def show(
            self,
            placeholder: Union[DeltaGenerator, None] = None
    ) -> None:
        """"""
        if isinstance(self.content, str) and self.display_type in ('markdown', 'image'):
            show_fun = get_show_fun(placeholder, self.display_type)
        elif isinstance(self.content, pd.DataFrame) and self.display_type == 'dataframe':
            show_fun = get_show_fun(placeholder, self.display_type)
        else:
            raise ValueError(f"<placeholder> not support content type: {type(self.content)}.")
        if self.display_info.get("expander"):
            with st.expander(**self.display_info.get("expander")):
                if self.display_info.get("tabs"):
                    tabs_info = self.display_info.get("tabs")
                    tabs = st.tabs(tabs_info.get("tabs"))
                    tabs_display_type = tabs_info.get("display_type")
                    tabs_data = tabs_info.get("data")
                    for i, tab in enumerate(tabs):
                        with tab:
                            show_fun = get_show_fun(
                                placeholder, display_type=tabs_display_type[i])
                            show_fun(tabs_data[i])
                else:
                    show_fun(self.content)
        else:
            show_fun(self.content)


def append_conversation(
        conversation: Conversation,
        messages: list[Conversation],
        placeholder: Union[DeltaGenerator, None] = None,
        **kwargs,
) -> None:
    """"""
    messages.append(conversation)
    conversation.show(placeholder)
    if kwargs.get("show_messages"):
        show_messages = kwargs.get("show_messages")
        show_messages.append(conversation)


def init_chat_history(
        init_message: Optional[str] = f"您好，您可以跟我对话，很高兴为您服务🥰。"
) -> Tuple[List[Conversation], List[Conversation]]:
    """"""
    if init_message:
        with st.chat_message("assistant", avatar='🤖'):
            st.markdown(init_message)

    if "show_messages" in st.session_state:
        with st.container():
            for message in st.session_state.show_messages:
                avatar = '🧑‍💻' if message.role == "user" else '🤖'
                with st.chat_message(message.role, avatar=avatar):
                    message.show(placeholder=st)
    else:
        st.session_state.messages = []
        st.session_state.show_messages = []
    return st.session_state.messages, st.session_state.show_messages
