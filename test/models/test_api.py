import os
import unittest
from openai import OpenAI
from zlai.types import ImageMessage, UserMessage


class TestModels(unittest.TestCase):
    def test_completion(self):
        """"""
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[
                UserMessage(content="Hello").model_dump(),
            ],
            stream=False
        )
        print(response)

    def test_completion_stream(self):
        """"""
        client = OpenAI(
            api_key="fake-api-key",
            base_url="http://localhost:8000"
        )

        stream = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[{"role": "user", "content": "hi"}],
            stream=True,
        )
        answer = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            answer += content
            print(content)
        print(answer)

    def test_completion_single_stream(self):
        """"""
        client = OpenAI(
            api_key="fake-api-key",
            base_url="http://localhost:8000/Qwen2-0.5B-Instruct"
        )

        response = client.chat.completions.create(
            model="Qwen2-0.5B-Instruct",
            messages=[{"role": "user", "content": "hi"}],
            stream=False,
        )
        print(response)

    def test_image_message(self):
        """"""
        url = "https://picx.zhimg.com/80/v2-0aea2c883dc1c8b8ca566eb8a8b38c70_720w.png"
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="glm-4v-9b",
            messages=[
                ImageMessage(content="介绍图片", images_url=[url]).model_dump(),
            ],
            stream=False
        )
        print(response)

    def test_function_call_messages(self):
        messages = [{'role': 'user',
          'content': "What's the Celsius temperature in San Francisco?"},
         {'content': None,
          'role': 'assistant',
          'function_call': None,
          'tool_calls': [{'id': 'call_dmfp59bEO3P12J5N1sBFSsxO',
                          'function': {'arguments': '{"location": "San Francisco, CA", "format": "celsius"}',
                                       'name': 'get_current_weather'},
                          'type': 'function'}]},
         {'role': 'observation',
          'content': '{San Francisco, CA: {celsius: 15}}',
          'function_call': True}]

        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.chat.completions.create(
            model="glm-4-9b-chat",
            messages=messages,
            stream=False
        )
        print(response)


class TestMiniCPM(unittest.TestCase):
    """"""
    def test_model(self):
        """"""
        url = "https://picx.zhimg.com/80/v2-0aea2c883dc1c8b8ca566eb8a8b38c70_720w.png"
        messages = [
            ImageMessage(content="介绍这个图片", images_url=[url]).to_dict(),
        ]
        client = OpenAI(api_key="1234", base_url=os.getenv("BASE_URL"))
        response = client.chat.completions.create(
            model="MiniCPM-V-2_6",
            messages=messages,
            stream=False
        )
        print(response)
