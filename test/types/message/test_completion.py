import unittest
from zlai.types.messages import ChatCompletionMessage
from zlai.types.function_call import ChatCompletionMessageToolCall, Function


class TestChatCompletionMessage(unittest.TestCase):

    def test_to_base_message(self):
        message = ChatCompletionMessage(
            role="assistant",
            content="None",
        )
        print(message.to_message())

    def test_to_function_call(self):
        message = ChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[ChatCompletionMessageToolCall(
                id="test",
                function=Function(arguments="{a: v}", name="test"),
                type="function",
            )],
        )
        print(message.to_message())

    def test_to_image_message(self):
        """"""
        content = [
            {'type': 'text', 'text': '解析图片中的文字'},
            {'type': 'image_url', 'image_url': {'url': '/MjIoL/8QAtRAAAgEDAwIEAwUFBA'}}
        ]
        message = ChatCompletionMessage(
            role="assistant",
            content=content,
        )
        image_message = message.to_message()
        print(type(image_message))
        print(image_message)

    def test_to_audio_message(self):
        """"""
        content = [
            {'type': 'text', 'text': '解析图片中的文字'},
            {'type': 'audio', 'audio_url': "dadsa"}
        ]
        message = ChatCompletionMessage(
            role="assistant",
            content=content,
        )
        audio_message = message.to_message()
        print(type(audio_message))
        print(audio_message)

