import unittest
from zlai.llms import LocalCompletion, GLM4Chat9BGenerateConfig


class TestLocalCompletion(unittest.TestCase):
    """"""
    def test_local_completion(self):
        """"""
        llm = LocalCompletion(generate_config=GLM4Chat9BGenerateConfig(stream=False), verbose=True)
        completion = llm.generate(query="1+1=")
        print(completion)

    def test_local_completion_stream(self):
        """"""
        llm = LocalCompletion(generate_config=GLM4Chat9BGenerateConfig(stream=True), verbose=True)
        completion = llm.generate(query="1+1=")
        answer = ""
        for chunk in completion:
            answer += chunk.choices[0].delta.content
            print(answer)
