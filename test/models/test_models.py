import yaml
import unittest
from zlai.models.completion import *
from zlai.models.types import *


class TestLoadModel(unittest.TestCase):
    def setUp(self):
        """"""
        with open('../../models_config.yml', 'r') as f:
            self.models_config = yaml.load(f, Loader=yaml.FullLoader).get("models_config")
        self.generate_config = StreamInferenceGenerateConfig()
        print(self.models_config)

    def test_completion(self):
        model_completion = LoadModelCompletion(
            models_config=self.models_config,
            model_name="Qwen2-0.5B-Instruct",
            verbose=True,
        )
        content = model_completion.completion(messages=[{"role": "user", "content": "hi"}])
        print(content)

    def test_stream_completion(self):
        model_completion = LoadModelCompletion(
            models_config=self.models_config,
            model_name="Qwen2-0.5B-Instruct",
            generate_config=StreamInferenceGenerateConfig(),
            verbose=True,
        )
        response = model_completion.stream_completion(messages=[{"role": "user", "content": "hi"}])
        answer = ""
        for content in response:
            answer += answer
            print(content)
        print(answer)

