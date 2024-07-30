import unittest
from zlai.models.completion import *


class TestLoadModel(unittest.TestCase):
    def test_load_model(self):
        model_completion = LoadModelCompletion(
            model_path="/home/models/Qwen/Qwen2-0.5B-Instruct",
            verbose=True,
        )
        content = model_completion.completion(messages=[{"role": "user", "content": "hi"}])
        print(content)
