import os
from io import BytesIO
import streamlit as st
from typing import Dict, Any, Iterable, Optional
from openai import OpenAI

from zlai.llms import TypeLLM
from zlai.types.messages import *
from zlai.types.messages.display import *
from zlai.types.function_call import ChatCompletionMessageToolCall
from zlai.streamlit.utils import avatar_mapping
from zlai.agent import Tools
from zlai.tools import transform_tool_params


__all__ = [
    "add_user_messages",
    "add_assistant_messages",
    "StreamlitChat",
]


chart_tools = [
    "base_chart", "pie_chart", "radar_chart", "scatter_chart", "map_chart"
]
image_tools = ["generate_image"]
audio_tools = ["generate_audio"]


def add_user_messages(
        content: str,
        image: Optional[TypeImage] = None,
        **kwargs,
):
    """"""
    if image:
        display_message = ImageMessage(role="user", content=content, images=[image])
        message = UserMessage(content=content)
    else:
        display_message = UserMessage(content=content)
        message = display_message
    st.session_state.display_messages.append(display_message)
    st.session_state.messages.append(message)


def add_assistant_messages(
        content: Optional[str] = None,
        image: Optional[TypeImage] = None,
        audio: Optional[Union[BytesIO, bytes]] = None,
        chart: Optional[str] = None,
        tool_call: Optional[ChatCompletionMessageToolCall] = None,
        observation: Optional[Union[str, Dict]] = None,
        tool_call_id: Optional[str] = None,
        **kwargs,
):
    """"""
    if image:
        display_message = ImageMessage(role="assistant", content=content, images=[image])
        message = AssistantMessage(content=content)
    elif audio:
        display_message = AudioMessage(role="assistant", content=content, audios=[audio])
        message = AssistantMessage(content=content)
    elif chart:
        display_message = ChartMessage(role="assistant", content=content, charts=[chart])
        message = AssistantMessage(content="已为您生成图表。")
    elif tool_call:
        display_message = ChatCompletionMessage(
            role="assistant", content=content, tool_calls=[tool_call])
        message = display_message
    elif tool_call_id and observation:
        display_message = ObservationMessage(content=observation)
        message = ToolsMessage(content=str(observation), tool_call_id=tool_call_id)
    elif observation:
        display_message = ObservationMessage(content=observation)
        message = display_message
    else:
        display_message = AssistantMessage(content=content)
        message = display_message
    st.session_state.display_messages.append(display_message)
    st.session_state.messages.append(message)


class StreamlitChat:
    tool_call: Optional[Union[Dict, ChatCompletionMessageToolCall]]

    def __init__(
            self,
            llm: Optional[TypeLLM] = None,
            model: Optional[str] = None,
            tools: Optional[Tools] = None,
            history: Optional[int] = 1,
    ):
        """"""
        self.llm = llm
        self.model = model
        self.tools = tools
        self.history = history
        self.tool_call = None
        self.not_observe_tools = chart_tools + image_tools + audio_tools

    def __call__(self, *args, **kwargs):
        """"""
        self.chat_base(**kwargs)
        self.chat_tools()
        self.chat_observation()

    def is_html(self, text: str) -> bool:
        """"""
        if "Traceback" in text:
            return False
        else:
            return True

    def generate(self) -> Iterable:
        """"""
        messages = [message.to_dict() for message in st.session_state.messages[-self.history:]]
        if isinstance(self.llm, TypeLLM):
            completion = self.llm.generate(messages=messages)
            return completion
        else:
            tools = None
            if self.tools is not None:
                tools = self.tools.tool_descriptions
            client = OpenAI(api_key="1", base_url=os.getenv("BASE_URL", "http://localhost:8000/"))
            completion = client.chat.completions.create(
                model=self.model, messages=messages, tools=tools,
                tool_choice="auto",
                stream=True,
            )
            return completion

    def dispatch_tools(self) -> Any:
        """"""
        try:
            tool_name = self.tool_call.function.name
            tool_params = eval(self.tool_call.function.arguments)
            tool_params = transform_tool_params(tool_params)
            data = self.tools.dispatch_tool(tool_name=tool_name, tool_params=tool_params)
            return data
        except Exception as e:
            return f"调用工具失败: {e}"

    def show_chart_observation(self, observation):
        """"""
        if self.is_html(observation):
            chart_message = ChartMessage(charts=[observation])
            chart_message.show_streamlit()
            self.add_assistant_messages(chart=observation)
        else:
            content = f"渲染图出错，请调整文本并重试。错误信息：\n{observation}"
            st.markdown(content)
            self.add_assistant_messages(content=content)

    def show_image_observation(self, observation):
        """"""
        if isinstance(observation, TypeImage):
            image_message = ImageMessage(images=[observation])
            image_message.show_streamlit()
            self.add_assistant_messages(image=observation)
        else:
            content = f"渲染图片出错，请调整文本并重试。错误信息：\n{observation}"
            st.markdown(content)
            self.add_assistant_messages(content=content)

    def show_audio_observation(self, observation):
        """"""
        if isinstance(observation, BytesIO):
            image_message = AudioMessage(audios=[observation])
            image_message.show_streamlit()
            self.add_assistant_messages(audio=observation)
        else:
            content = f"渲染声音出错，请调整文本并重试。错误信息：\n{observation}"
            st.markdown(content)
            self.add_assistant_messages(content=content)

    def chat_base(self, content: str):
        """"""
        with st.chat_message("user", avatar=avatar_mapping.get("user")):
            st.markdown(content)
        self.add_user_messages(content=content)
        with st.chat_message("assistant", avatar=avatar_mapping.get("assistant")):
            placeholder = st.empty()
            content = ""
            completion = self.generate()
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    placeholder.markdown(content)
                if chunk.choices[0].delta.tool_calls is not None:
                    self.tool_call = chunk.choices[0].delta.tool_calls[0].model_dump()
                    self.tool_call = ChatCompletionMessageToolCall.model_validate(self.tool_call)

            if content != "":
                self.add_assistant_messages(content=content)
            if self.tool_call is not None:
                show_tool_call(tool_call=self.tool_call)
                self.add_assistant_messages(tool_call=self.tool_call)

    def chat_tools(self):
        """"""
        if self.tool_call is not None:
            with st.chat_message("observation", avatar=avatar_mapping.get("observation")):
                observation = self.dispatch_tools()
                if self.tool_call.function.name in chart_tools:
                    self.show_chart_observation(observation)
                elif self.tool_call.function.name == "generate_image":
                    self.show_image_observation(observation)
                elif self.tool_call.function.name == "generate_audio":
                    self.show_audio_observation(observation)
                else:
                    show_observation(observation)
                    self.add_assistant_messages(observation=observation, tool_call_id=self.tool_call.id)

    def chat_code(self):
        """"""

    def chat_observation(self):
        """"""
        if self.tool_call is not None and self.tool_call.function.name not in self.not_observe_tools:
            with st.chat_message("assistant", avatar=avatar_mapping.get("assistant")):
                placeholder = st.empty()
                content = ""
                completion = self.generate()
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        content += chunk.choices[0].delta.content
                        placeholder.markdown(content)
                self.add_assistant_messages(content=content)

    def add_user_messages(self, **kwargs: Any):
        """"""
        add_user_messages(**kwargs)

    def add_assistant_messages(self, **kwargs: Any):
        """"""
        add_assistant_messages(**kwargs)
