from zlai.llms import Zhipu, GLM4AirGenerateConfig, GLM4FlashGenerateConfig, GLM4GenerateConfig, TypeLLM
import streamlit as st


__all__ = ["sidebar"]


def sidebar() -> TypeLLM:
    """"""
    with st.sidebar:
        top_p = st.slider("top_p", 0.0, 0.99, 0.7, step=0.01)
        temperature = st.slider("temperature", 0.0, 0.99, 0.95, step=0.01)
        max_tokens = st.slider("max_new_tokens", 1, 8192, 2048, step=10)

        models = [
            GLM4GenerateConfig(max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True),
            GLM4AirGenerateConfig(max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True),
            GLM4FlashGenerateConfig(max_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True),
        ]
        options = [model.model for model in models]
        select_box = st.sidebar.selectbox(label="选择对话大模型", index=1, options=options,)
        llm = Zhipu(generate_config=models[options.index(select_box)])

        cols = st.columns(2)
        export_btn = cols[0]
        clear_history = cols[1].button("Clear", use_container_width=True)
        retry = export_btn.button("Retry", use_container_width=True)
    return llm
