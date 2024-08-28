import unittest
from zlai.llms import LocalCompletion
from zlai.types.generate_config.completion import GLM4GenerateConfig


class TestLocalCompletion(unittest.TestCase):
    """"""
    def test_local_completion(self):
        """"""
        llm = LocalCompletion(model="glm-4-9b-chat", generate_config=GLM4GenerateConfig(), stream=False, verbose=True)
        completion = llm.generate(query="1+1=")
        print(completion)

    def test_local_completion_stream(self):
        """"""
        llm = LocalCompletion(model="glm-4-9b-chat", generate_config=GLM4GenerateConfig(), stream=True, verbose=True)
        completion = llm.generate(query="1+1=")
        answer = ""
        for chunk in completion:
            answer += chunk.choices[0].delta.content
            print(answer)
