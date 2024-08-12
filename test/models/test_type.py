import unittest
from zlai.models.types import ModelConfig


class TestType(unittest.TestCase):
    """"""

    def test_type(self, ):
        """"""
        data = {
            'model_name': 'kolors_image2image',
            'model_path': '/home/models/Kwai-Kolors/Kolors-diffusers',
            'model_type': 'diffuser_image2image',
            'load_method': 'load_kolors_image2image',
            'generate_method': 'KolorsImage2ImageGenerateConfig', 'max_memory': {0: '32GB'}}

        config = ModelConfig.model_validate(data)
        print(config)
