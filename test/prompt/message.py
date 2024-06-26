import unittest
from zlai.schema import ImagePrompt


class TestImagePrompt(unittest.TestCase):
    def test_image_prompt(self):
        """"""
        img_prompt = ImagePrompt(image='test.png', content='这是什么')
        print(img_prompt.dict())

