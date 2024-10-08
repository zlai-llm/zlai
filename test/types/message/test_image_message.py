import unittest
import io, base64
from PIL import Image
from typing import List, Dict
from zlai.types.messages import *


class TestImageMessage(unittest.TestCase):
    """"""

    def setUp(self):
        self.path = "/Users/chensy/Pictures/TGWX8088-opq570071353.jpg"
        self.url = "https://picx.zhimg.com/80/v2-0aea2c883dc1c8b8ca566eb8a8b38c70_720w.png"

    def test_image_format(self):
        """"""
        path = "/Users/chensy/Downloads/智能机器人.png"
        image = Image.open(path)
        image_message = ImageMessage(content="介绍这个图片", images=[image])
        # print(image_message)
        print(image_message.to_dict())

    def test_image_message_path(self):
        """"""
        image_message = ImageMessage(content="介绍这个图片", images_url=[self.url], images_path=[self.path])
        for k, v in image_message.model_dump().items():
            print(k, len(v))
        print(type(image_message.content))
        for item in image_message.content:
            if item.type == "image_url":
                print(item.type, len(item.image_url.url))
            else:
                print(item)

    def test_image_mini_cpm_message(self):
        """"""
        from PIL import Image
        image = Image.open(self.path)

        image_message = ImageMessage(
            content="介绍这个图片", images=[image], images_url=[self.url], images_path=[self.path])
        print(image_message.to_message(_type="mini_cpm"))
        print(image_message.to_message(_type="glm4v"))

    def test_images(self):
        from PIL import Image
        image = Image.open(self.path)

        image_message = ImageMessage(
            content="介绍这个图片", images=[image])
        print(image_message.to_message(_type="mini_cpm"))
        print(image_message.to_message(_type="glm4v"))
        print(image_message.to_message(_type="qwen2vl"))
