from typing import Optional
import streamlit as st


__all__ = [
    "avatar_mapping",
    "init_chat_history",
]


avatar_mapping = {
    "system": "🧠",
    "user": "🧑",
    "assistant": "🤖",
    "observation": "💡",
}


def init_chat_history(
        init_message: Optional[str] = None
):
    """"""
    if init_message:
        with st.chat_message("assistant", avatar='🤖'):
            st.markdown(init_message)

    if "display_messages" in st.session_state:
        with st.container():
            for message in st.session_state.display_messages:
                role = message.role
                avatar = avatar_mapping.get(role)
                with st.chat_message(role, avatar=avatar):
                    message.show_streamlit()
    else:
        st.session_state.messages = []
        st.session_state.display_messages = []
