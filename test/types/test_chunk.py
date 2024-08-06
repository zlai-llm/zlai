import time
import unittest
from zlai.types.chat.chat_completion_chunk import *
from zlai.models.completion.glm4 import ParseFunctionCall

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


class TestChunk(unittest.TestCase):
    """"""
    def test_chunk(self):
        """"""
        choice_delta = ChoiceDelta(role="assistant", content="")
        finish_reason = "stop"

        chunk_choice = Choice(finish_reason=finish_reason, index=0, delta=choice_delta)
        chat_completion_chunk = ChatCompletionChunk(
            id="_id", created=int(time.time()), model="self.model_name", choices=[chunk_choice]
        )
        print(chat_completion_chunk)

    def test_chunk_function_call(self):
        """"""
        content = """get_current_weather\n{"location": "San Francisco, CA", "format": "celsius"}"""
        parse_function_call = ParseFunctionCall(content=content, tools=tools)
        chat_completion_message = parse_function_call.to_stream_completion_delta()
        print(chat_completion_message)
        choice_delta = ChoiceDelta.model_validate(chat_completion_message.model_dump())
        print(choice_delta)

