from pydantic import BaseModel
import streamlit as st
from zlai.llms import *
from zlai.agent import *
from zlai.streamlit import *


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


# llm = Zhipu(generate_config=ZhipuGLM3Turbo())
# llm = LocalLLMAPI(generate_config=Qwen15Chat14BGenerateConfig())

def sidebar() -> TypeLLM:
    """"""
    models = [
        GLM4GenerateConfig(stream=True),
        GLM4AirGenerateConfig(stream=True),
        GLM4FlashGenerateConfig(stream=True),
    ]
    options = [model.model for model in models]
    select_box = st.sidebar.selectbox(label="选择对话大模型", index=1, options=options,)
    llm = Zhipu(generate_config=models[options.index(select_box)])
    return llm


def clear_page_config():
    """"""
    if st.session_state.get('page_name') != page_config.page_name:
        st.session_state.clear()
        st.session_state['page_name'] = page_config.page_name


def main():
    clear_page_config()
    llm = sidebar()
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
