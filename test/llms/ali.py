import unittest
from zlai.schema import UserMessage
from zlai.llms.ali import *
from zlai.llms.generate_config.api.ali import *


class TestMokeAliModels(unittest.TestCase):
    """"""
    def test_loop_config(self):
        """"""
        config = [
            AliQwen2Instruct57BA14BGenerateConfig,
            AliQwen2Instruct72BGenerateConfig,
            AliQwenInstruct27BGenerateConfig,
            AliQwen2Instruct15BGenerateConfig,
            AliQwen2Instruct05BGenerateConfig,
        ]
        for gen_config in config:
            print(gen_config.__name__)
            llm = Ali(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(data.output.choices[0].message.content)



class TestAli(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.config_ali = AliQwen15Chat7BGenerateConfig()
        self.llm = Ali(
            generate_config=self.config_ali,
        )

    def test_qwen_7b(self):
        """"""
        output = self.llm.generate(query="你好")
        print(output)

    def test_stream_qwen_7b(self):
        """"""
        self.config_ali = AliQwen15Chat7BGenerateConfig(stream=True)
        self.llm = Ali(generate_config=self.config_ali)

        responses = self.llm.generate(query="你好")
        answer = ''
        for response in responses:
            answer += response.output.choices[0].message.content
            print(answer)

    def test_parse_dict(self):
        self.config_ali = AliQwen15Chat7BGenerateConfig(stream=False)
        self.llm = Ali(generate_config=self.config_ali)
        output = self.llm.generate_with_parse(
            query="请输出一个简短的dict。有两个key: name/age",
            parse_dict='eval',
        )
        print(self.llm.parse_info)
        print(output)

    def test_qwen_message(self):
        """"""
        messages = [UserMessage(content="你好")]
        output = self.llm.generate(messages=messages)
        print(output)

