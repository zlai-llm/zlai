import unittest
from zlai.models.types import ModelConfig


class TestModelConfig(unittest.TestCase):
    """"""
    def test_model_config(self):
        data = {
            "model_name": "Qwen2-0.5B-Instruct",
            "model_path": "/home/models/Qwen/Qwen2-0.5B-Instruct",
            "model_type": "completion",
            "load_method": "load_qwen2",
            # "generate_method": "Qwen205BInstructInferenceGenerateConfig",
            "max_memory": {0: "2GB"}
        }
        model_config = ModelConfig.model_validate(data)
        print(model_config)
