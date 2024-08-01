import unittest
from zlai.types.messages import ImageMessage


class TestImageMessage(unittest.TestCase):
    """"""

    def setUp(self):
        self.path = "/Users/chensy/Pictures/TGWX8088-opq570071353.jpg"
        self.url = "https://picx.zhimg.com/80/v2-0aea2c883dc1c8b8ca566eb8a8b38c70_720w.png"

    def test_image_message_path(self):
        """"""
        image_message = ImageMessage(content="介绍这个图片").add_image(path=self.path)
        for key, val in image_message.model_dump().items():
            print(key, len(val))
        image_message.split_image()
        print(image_message)
        # image_message.write_image(data=image_message.image, path="./test.png")

    def test_image_message_url(self):
        """"""
        image_message = ImageMessage(content="介绍这个图片").add_image(url=self.url)
        for key, val in image_message.model_dump().items():
            print(key, len(val))


