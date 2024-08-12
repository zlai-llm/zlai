import unittest
from openai import OpenAI


class TestImagesEdits(unittest.TestCase):
    """"""
    def test_images_edit(self):
        """"""
        client = OpenAI(api_key="1234", base_url="http://127.0.0.1:8000/")
        response = client.images.edit(
            model="kolors_image2image",
            image=open("/Users/chensy/Downloads/智能机器人.png", "rb"),
            prompt="A sunlit indoor lounge area with a pool containing a flamingo",
            n=1,
            size="1024x1024"
        )
        print(response)
