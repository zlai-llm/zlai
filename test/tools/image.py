import os
import unittest
from zlai.agent import Tools
from zlai.tools import generate_audio, generate_image
from zlai.types.messages import *
from openai import OpenAI


class TestImageAudioAgent(unittest.TestCase):
    """"""
    def test_import(self):
        """"""
        from zlai.agent import Tools

    def test_image(self):
        """"""
        tools = Tools(tool_list=[generate_audio, generate_image])
        client = OpenAI(api_key="1", base_url=os.getenv("BASE_URL"))

        messages = [UserMessage(content="请画一张猫的图片").to_dict()]
        completion = client.chat.completions.create(
            model="glm-4-9b-chat",
            messages=messages,
            tools=tools.tool_descriptions,
            tool_choice="auto",
            stream=True,
        )

        answer = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                answer += content
                print(answer)
        print(chunk)

    def test_dispatch(self):
        """"""
        data = {
            "prompt": "一只可爱的猫，毛茸茸的，眼睛大大的，表情温柔，高清，色彩鲜艳，分辨率4K，卡通风格。"
        }
        tools = Tools(tool_list=[generate_audio, generate_image])
        data = tools.dispatch_tool(tool_name="generate_image", tool_params=data)
        print(data)
