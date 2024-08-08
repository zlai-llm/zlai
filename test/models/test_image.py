import unittest


class TestImage(unittest.TestCase):
    """"""
    from openai import OpenAI
    client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")

    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1, response_format="b64_json",
    )
    print(response)


