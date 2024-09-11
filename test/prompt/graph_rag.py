import unittest
from zlai.prompt.graph import prompt_entities, prompt_relations
from zlai.llms import Zhipu
from zlai.llms.generate_config.api import GLM4FlashGenerateConfig


class TestGraphRAG(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4FlashGenerateConfig())
        with open("../test_data/xiyouji/test.md", "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_prompt_entities(self):
        """"""
        entity_types = ["人物"]
        message = prompt_entities.format_prompt(
            content=self.content, entity_types=str(entity_types)
        ).to_messages(role="user")
        completion = self.llm.generate(messages=[message])
        print(completion.choices[0].message.content)

        message = prompt_relations.format_prompt(
            content=self.content, entity_types=str(entity_types),
            entities=completion.choices[0].message.content,
        ).to_messages(role="user")
        completion = self.llm.generate(messages=[message])
        print(completion.choices[0].message.content)

    def test_split_content(self):
        """"""
        with open("../test_data/xiyouji/西游记.md", "r", encoding="utf-8") as f:
            content = f.read()
        content = content.split("\n\n\n\n")
        content = [item for item in content if len(item.strip()) > 0]
        print(len(content))
        print(max([len(item) for item in content]))
