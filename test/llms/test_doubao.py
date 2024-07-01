import unittest
from zlai.llms import DouBao, OpenAIGenerateConfig


class TestDouBao(unittest.TestCase):
    """"""
    def test_doubao(self):
        """"""
        models = [
            "ep-20240630100146-r89zj",
            "ep-20240630100032-29bh9",
            "ep-20240630100000-xvz2b",
            "ep-20240630095928-f9fl7",
            "ep-20240630095857-p9kbd",
            "ep-20240630095730-6c7sc",
        ]

        for model in models:
            llm = DouBao(generate_config=OpenAIGenerateConfig(model=model))
            completion = llm.generate("1+1=")
            print(completion.choices[0].message.content)
            print()
