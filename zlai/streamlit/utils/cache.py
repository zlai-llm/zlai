import streamlit as st


__all__ = ["clear_page_history"]


def clear_page_history():
    """"""
    if st.session_state.get("messages"):
        del st.session_state.messages
    if st.session_state.get("display_messages"):
        del st.session_state.display_messages
    st.success("Chat history cleared!")
