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

