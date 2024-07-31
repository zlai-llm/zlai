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
