import unittest
from zlai.models.types.images_generations import TypeImageGenerateConfig, ImageGenerateConfig


class TestImageGenerateConfig(unittest.TestCase):
    def test_image_generate_config(self):
        class ImageGenerateConfig:
            def __init__(self, width: int, height: int):
                self.width = width
                self.height = height

        class KolorsImageGenerateConfig:
            def __init__(self, palette: list):
                self.palette = palette

        from typing import Union

        TypeImageGenerateConfig = Union[ImageGenerateConfig, KolorsImageGenerateConfig]

        image_config = ImageGenerateConfig(width=256, height=256)
        colors_config = KolorsImageGenerateConfig(palette=['#FF0000', '#00FF00', '#0000FF'])

        print(isinstance(image_config, TypeImageGenerateConfig))  # True
        print(isinstance(colors_config, TypeImageGenerateConfig))  # True
        # print(isinstance(ImageGenerateConfig(), TypeImageGenerateConfig))
