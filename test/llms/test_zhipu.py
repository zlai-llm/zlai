import unittest
from zlai.llms.zhipu import *
from zlai.llms.generate_config.api.zhipu import *


class TestMokeZhipuModels(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_legal_person",
                    "description": "根据提供的公司名称，查询该公司对应的法人代表。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "company_name": {
                                "type": "string",
                                "description": "公司名称",
                            }
                        },
                        "required": ["company_name"],
                    },
                }
            }
        ]

    def test_loop_config(self):
        """"""
        config = [
            GLM4GenerateConfig,
            GLM40520GenerateConfig,
            GLM4AirGenerateConfig,
            GLM4AirXGenerateConfig,
            GLM4FlashGenerateConfig,
            GLM3TurboGenerateConfig,
            CodeGeexGenerateConfig,
        ]
        for gen_config in config:
            print(gen_config.__name__)
            llm = Zhipu(generate_config=gen_config())
            data = llm.generate(query="1+1=")
            print(data.choices[0].message.content)

    def test_glm_3_turbo(self):
        llm = Zhipu(generate_config=GLM3TurboGenerateConfig())
        data = llm.generate(query="1+1=")
        print(data.choices[0].message.content)

    def test_glm_4(self):
        """"""
        llm = Zhipu(generate_config=GLM4GenerateConfig())
        data = llm.generate(query="1+1=")
        print(data.choices[0].message.content)

    def test_glm_4_long(self):
        """"""
        llm = Zhipu(generate_config=GLM4LongGenerateConfig())
        completion = llm.generate(query="1+1=")
        print(completion.model)
        print(completion.choices[0].message.content)

    def test_glm_4_9b(self):
        """"""
        llm = Zhipu(generate_config=GLM49BGenerateConfig())
        data = llm.generate(query="1+1=")
        print(data.choices[0].message.content)

    def test_glm_4_flash(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())
        data = llm.generate(query="1+1=")
        print(data.choices[0].message.content)

    def test_web_search(self):
        web_search_tool = {
            "type": "web_search",
            "web_search": {
                "enable": True,
                "search_result": True,
            }
        }
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig(tools=[web_search_tool]))
        query = "什么是审计失败和其法律责任？"
        data = llm.generate(query=query)
        print(data)
        print(data.choices[0].message.content)
        print()

        llm = Zhipu(generate_config=GLM4FlashGenerateConfig(tools=[]))
        data = llm.generate(query=query)
        print(data)
        print(data.choices[0].message.content)

    def test_tools(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig(tools=self.tools))
        completion = llm.generate(query="我想要联系广州发展集团股份有限公司公司的法人代表，请问他的名字是什么？")
        print(completion)
        print(completion.choices[0].message.tool_calls[0].id)

    def test_tools_stream(self):
        """"""
        llm = Zhipu(generate_config=GLM4GenerateConfig(tools=self.tools, stream=True))
        output = llm.generate(query="我想要联系广州发展集团股份有限公司公司的法人代表，请问他的名字是什么？")
        answer = ''
        for out in output:
            print(out)
            answer += out.choices[0].delta.content
            print(answer)

    def test_tools_stream2(self):
        """"""
        messages = [
            {'role': 'assistant', 'content': None, 'function_call': None, 'tool_calls': [{'id': 'call_2024082711153920bd346496c04e45', 'function': {'arguments': '{"fund_code":"008888"}', 'name': 'search_fund'}, 'type': 'function'}]},
            {'role': 'tool', 'content': "[{'基金代码': '008888', '基金拼音简写': 'HXGZBDTXPETFLJC', '基金名称': '华夏国证半导体芯片ETF联接C', '基金类': '指数型-股票', '基金拼音全称': 'HUAXIAGUOZHENGBANDAOTIXINPIANETFLIANJIEC'}]", 'tool_call_id': 'call_2024082711153920bd346496c04e45'}]


        llm = Zhipu(generate_config=GLM4GenerateConfig(tools=self.tools, stream=True))
        output = llm.generate(query="我想要联系广州发展集团股份有限公司公司的法人代表，请问他的名字是什么？")
        answer = ''
        for out in output:
            print(out)
            answer += out.choices[0].delta.content
            print(answer)

class TestZhipu(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.config_glm3 = GLM3TurboGenerateConfig()
        self.llm = Zhipu(generate_config=self.config_glm3)

    def test_glm3_async(self):
        """"""
        outputs = self.llm.async_generate(query_list=["你好", "你好"])
        print(outputs)

    def test_stream_glm3(self):
        """"""
        self.config_glm3 = GLM3TurboGenerateConfig(stream=True)
        self.llm = Zhipu(generate_config=self.config_glm3,)
        output = self.llm.generate(query="你好")
        answer = ''
        for out in output:
            answer += out.choices[0].delta.content
            print(answer)

    def test_parse_dict(self):
        self.config_glm3 = GLM3TurboGenerateConfig(stream=False)
        self.llm = Zhipu(generate_config=self.config_glm3, )
        output = self.llm.generate_with_parse(
            query="请输出一个简短的dict。有两个key: name/age",
            parse_dict='eval',
        )
        print(self.llm.parse_info)
        print(output)

    def test_udf_parse_dict(self):
        """"""
        from zlai.llms import Zhipu, GLM3TurboGenerateConfig

        def udf_parse(string):
            """自定义解析函数"""
            return eval(string)

        llm = Zhipu(generate_config=GLM3TurboGenerateConfig())
        question = """
        文本：张三在杭州吃了一笼小笼包。
        问题：请解析出文本中的人名、地点，以Dict的格式输出。
        格式示例：{'name': ..., 'place': ...,}
        你只需要输出解析后的Dict，不需要输出其他内容。"""
        output = llm.generate_with_parse(query=question, parse_fun=udf_parse)
        print(llm.parse_info)
        print(f"解析后数据类型: {type(output[0])}")
        print(f"解析结果: {output[0]}")


class TestGLM4V(unittest.TestCase):
    """"""
    def setUp(self):
        self.url = "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"

    def test_message(self):
        """"""
        message = ZhipuImageMessage(content="介绍这个图片").add_image(url=self.url)
        print(message)

    def test_generate(self):
        """"""
        llm = Zhipu(generate_config=GLM4VGenerateConfig())
        messages = [ZhipuImageMessage(content="介绍这个图片").add_image(url=self.url)]
        completion = llm.generate(messages=messages)
        print(completion.choices[0].message.content)
