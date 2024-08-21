import unittest
from zlai.types.generate_config.deepseek import DeepSeekV2LiteChatGenerateConfig

class TestDeepSeek(unittest.TestCase):
    """"""
    def test_config(self):
        config = DeepSeekV2LiteChatGenerateConfig.model_validate({"temperature": None})
        print(config)
