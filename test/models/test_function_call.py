import time
import unittest
from zlai.models.completion.glm4 import *
from zlai.types import *


tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "format": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use. Infer this from the users location.",
                            },
                        },
                        "required": ["location", "format"],
                    },
                }
            },
        ]


class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        """"""

    def test_message_process(self):
        """"""
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content="你好"),
            AssistantMessage(content="你好"),
        ]
        process_messages = ProcessMessages(
            messages=messages, tools=tools, tool_choice="auto")
        print(process_messages.to_dict())

    def test_message_process_no_system(self):
        """"""
        messages = [
            UserMessage(content="你好"),
        ]
        process_messages = ProcessMessages(
            messages=messages, tools=tools, tool_choice="auto")
        print(process_messages.to_dict())

    def test_empty_message(self):
        """"""
        messages = []
        process_messages = ProcessMessages(
            messages=messages, tools=tools, tool_choice="auto")
        print(process_messages.to_dict())

    def test_image_message(self):
        """"""
        url = "https://picx.zhimg.com/80/v2-0aea2c883dc1c8b8ca566eb8a8b38c70_720w.png"
        messages = [
            UserMessage(content="你好"),
            ImageMessage(content="介绍图片").add_image(url=url),
        ]
        process_messages = ProcessMessages(
            messages=messages, tools=None, tool_choice="none")
        messages = process_messages.to_messages()
        messages = trans_messages(messages=messages)
        print(messages)

    def test_function_call(self):
        """"""
        pass


class TestParseFunctionCall(unittest.TestCase):
    def test_parse_function_call(self):
        """"""
        content = """get_current_weather\n{"location": "San Francisco, CA", "format": "celsius"}"""
        parse_function = ParseFunctionCall(tools=tools, content=content)
        function_call_params = parse_function.parse()
        print(function_call_params)

    def test_to_chat_completion_message(self):
        """"""
        content = """get_current_weather\n{"location": "San Francisco, CA", "format": "celsius"}"""
        content = """get_current_weather"""
        parse_function = ParseFunctionCall(tools=tools, content=content)
        chat_completion_message = parse_function.to_chat_completion_message()
        print(chat_completion_message)
        print(Choice(finish_reason="stop", index=0, message=chat_completion_message))
        chat_completion = ChatCompletion(
            id="1337",
            object="chat.completion",
            created=int(time.time()),
            model="request.model",
            choices=[Choice(finish_reason="stop", index=0, message=chat_completion_message)]
        )
        print(chat_completion)

