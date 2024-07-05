import unittest
from pydantic import BaseModel, Field
from typing import Optional
from zlai.agent.parse import ParseAgent
from zlai.schema import UserMessage, SystemMessage
from zlai.llms import Zhipu, GLM4AirGenerateConfig
from zlai.parse import ParseDict


class TestParseAgent(unittest.TestCase):
    """"""
    def setUp(self):
        self.llm = Zhipu(generate_config=GLM4AirGenerateConfig())
        self.system_prompt = SystemMessage(content="""你是一个解析器，根据用户输入，解析出用户的信息，并返回json格式。在下面的问答中，需要你解析出文本中的城市信息。""")
        self.few_shot = [
            UserMessage(content="张三明天去北京。"),
            UserMessage(content=str({"city": "北京"})),
        ]

    def test_parse(self):
        agent = ParseAgent(
            llm=self.llm,
            parse_fun=ParseDict.eval_dict,
            system_prompt=self.system_prompt,
            few_shot=self.few_shot)
        task_completion = agent("张三明天去上海。")
        print(task_completion.content)
        print(task_completion.parsed_data)

    def test_parse_schema(self):
        """"""
        class City(BaseModel):
            city: Optional[str] = Field(default=None, description="城市")

        agent = ParseAgent(
            llm=self.llm,
            parse_fun=ParseDict.eval_dict,
            system_prompt=self.system_prompt,
            few_shot=self.few_shot,
            output_schema=City,
        )
        task_completion = agent("张三明天去上海。")
        print(task_completion.content)
        print(f"Type: {type(task_completion.parsed_data)} Data: {task_completion.parsed_data}")

    def test_parse_schema_with_description(self):
        """"""
        few_shot = [
            UserMessage(content="张三明天去北京。"),
            UserMessage(content=str({"城市": "北京"})),
        ]

        class City(BaseModel):
            city: Optional[str] = Field(default=None, description="城市")

        agent = ParseAgent(
            llm=self.llm,
            parse_fun=ParseDict.eval_dict,
            system_prompt=self.system_prompt,
            few_shot=few_shot,
            output_schema=City,
            schema_key="description",
        )
        task_completion = agent("张三明天去上海。")
        print(task_completion.content)
        print(f"Type: {type(task_completion.parsed_data)} Data: {task_completion.parsed_data}")
