from PIL import Image
from io import BytesIO
from pydantic import BaseModel
import streamlit as st
from zlai.llms import *
from zlai.agent import *
from zlai.streamlit import *
from zlai.streamlit.web.pages.utils.chat import *


class PageConfig(BaseModel):
    """"""
    page_name: str = "ZLAI·Chat"


page_config = PageConfig()
st.set_page_config(
    page_title=page_config.page_name,
    page_icon=":robot:",
    layout='centered',
    initial_sidebar_state='expanded',
)
st.title(page_config.page_name)


def clear_page_config():
    """"""
    if st.session_state.get('page_name') != page_config.page_name:
        st.session_state.clear()
        st.session_state['page_name'] = page_config.page_name


def main():
    clear_page_config()
    llm = sidebar()

    uploaded_image = st.file_uploader(
        "上传图片",
        type=["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
        accept_multiple_files=False,
    )
    if uploaded_image:
        data: bytes = uploaded_image.read()
        image = Image.open(BytesIO(data)).convert("RGB")
        st.session_state.uploaded_image = image
    else:
        st.session_state.uploaded_image = None

    messages, show_messages = init_chat_history(
        init_message="你好，我是Chat，有什么可以帮助你的吗？")
    if question := st.chat_input("Shift + Enter 换行, Enter 发送"):
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(question)
        messages.append(Conversation(role="user", content=question))
        show_messages.append(Conversation(role="user", content=question))
        with st.chat_message("assistant", avatar='🤖'):
            placeholder = st.empty()
            completion = llm.generate(query=question)
            content = ""
            for resp in completion:
                content += resp.choices[0].delta.content
                placeholder.markdown(content)
            messages.append(Conversation(role="assistant", content=content))
            show_messages.append(Conversation(role="assistant", content=content))
        st.button("清空对话", on_click=clear_chat_history)


if __name__ == "__main__":
    main()
