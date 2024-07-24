import unittest
from zlai.llms import Zhipu, GLM4AirGenerateConfig
from zlai.agent import TaskParameters
from zlai.prompt import summary_prompt


class TestTaskParameters(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4AirGenerateConfig())

    def test_parameters(self):
        """"""
        task_parameters = TaskParameters(
            prompt_template=summary_prompt,
        )
        print(task_parameters.params())

