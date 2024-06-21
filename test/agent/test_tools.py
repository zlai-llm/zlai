import unittest
from typing import Annotated
from zlai.llms import Zhipu, GLM4FlashGenerateConfig
from zlai.agent import ToolsAgent
from zlai.agent.agent import register_tool

TEST_TOOL_HOOKS = {}
TEST_TOOL_DESCRIPTIONS = []


@register_tool(tool_hooks=TEST_TOOL_HOOKS, tool_descriptions=TEST_TOOL_DESCRIPTIONS)
def random_number_generator(
        seed: Annotated[int, "The random seed used by the generator", True],
        range: Annotated[tuple[int, int], "The range of the generated numbers", True],
) -> int:
    """
    Generates a random number x, s.t. range[0] <= x < range[1]
    """
    if not isinstance(seed, int):
        raise TypeError("Seed must be an integer")
    if not isinstance(range, tuple):
        raise TypeError("Range must be a tuple")
    if not isinstance(range[0], int) or not isinstance(range[1], int):
        raise TypeError("Range must be a tuple of integers")
    import random
    return random.Random(seed).randint(*range)


class TestToolsAgent(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4FlashGenerateConfig(tools=TEST_TOOL_DESCRIPTIONS))

    def test_(self):
        """"""
        tools = ToolsAgent(llm=self.llm, hooks=TEST_TOOL_HOOKS)
        completion = tools("生成一个10-17之间的随机数")
        print(completion)


