import unittest
import numpy as np
from zlai.llms import Zhipu, GLM4GenerateConfig, GLM4AirGenerateConfig, GLM4FlashGenerateConfig
from zlai.agent.tools import *
from zlai.tools import *
from zlai.schema import SystemMessage


class TestToolsAgent(unittest.TestCase):
    """"""
    def test_trans_data(self):
        """"""
        data = {'data': {'比亚迪': 100, '特斯拉': 200, '理想': 400, '蔚来': 300}, 'sub_title': '数据来源：大黄蜂汽车资讯', 'title': '比亚迪、特斯拉、蔚来、理想的4月份销量'}
        data = transform_tool_params(data)
        print(data)

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())

        tools = Tools(tool_list=[get_weather, random_number_generator])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("输出一个0-6的随机数？")
        print(task_completion.content)

    def test_charts_agent(self):
        """"""
        system_message = SystemMessage(content="You are a data drawing robot.")
        llm = Zhipu(generate_config=GLM4GenerateConfig())
        # llm = Zhipu(generate_config=GLM4FlashGenerateConfig())
        # llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        tools = Tools(tool_list=[base_chart, pie_chart, radar_chart, scatter_chart, map_chart], params_fun=transform_tool_params)
        agent = ToolsAgent(llm=llm, tools=tools, system_message=system_message, verbose=True)

        # task_completion = agent("汉东省2024年一季度的GDP数据为1.2万亿、2.3万亿、4.5万亿，请依据这些数据，绘制一个折线图，数据来源。")
        # task_completion = agent("汉东省2024年一季度的GDP数据为1.2万亿、2.3万亿、4.5万亿，请依据这些数据，绘制一个柱状图，数据来源。")
        # task_completion = agent("比亚迪、特斯拉、蔚来、理想的4月份销量数据为100、200、300、400，请依据这些数据，绘制一个饼图，数据来源（大黄蜂汽车资讯）。")
        task_completion = agent("2024年一季度的河北省、河南省、浙江省、广东省粮食收获数据为5.2亿吨、7.3亿吨、2.5亿吨、3.5亿吨，绘制一个地图清晰展示该数据，数据来源（农业部）。")
        # task_completion = agent("三国武将的谋略、武力、道德、攻速、领导力数据分别是，吕布（56, 99, 40, 67, 47）、关羽（89, 92, 99, 82, 95）、张飞（47, 89, 85, 67, 73）、赵云（86, 91, 87, 98, 69），请绘制雷达图展示。")
        # data = np.random.randint(high=10, low=0, size=(5, 2)).tolist()
        # task_completion = agent(f"请绘制一个散点图展示，数据为{data}。")
        print(task_completion.content)


class TestTools(unittest.TestCase):
    """"""
    def test_fund_agent(self):
        import inspect
        fund_agent = FundAgent(verbose=True)
        print(inspect.signature(fund_agent.dispatch_fun).parameters)
        data = fund_agent.dispatch_fun("get_current_fund_data", {'fund_code': '000001'})
        print(data)

    def test_fund_dispatch(self):
        """"""
        tool_calls = {
            "id": "call_8231168139794583938",
            "index": 0,
            "type": "function",
            "function": {
                "arguments": '{"fund_code": "000001"}',
                "name": "get_current_fund_data"
            }
        }
        tool_name = tool_calls.get('function').get("name")
        tool_params = eval(tool_calls.get('function').get("arguments"))
        out = fund_tools(tool_name=tool_name, tool_params=tool_params)
        print(out)

    def test_agent_call(self):
        """"""
        messages = [
            UserPrompt(content='请帮我查找000001的最新信息。').model_dump(),
        ]

        api = RemoteLLMAPI(remote=Remote.zhipu, api_key_path=self.api_key_path)
        gen_config = ZhipuGenerateConfig(
            tools=get_fund_tools(),
            tool_choice='auto',
        )
        api.set_model(model_name=ZhipuModel.glm_3_turbo)
        api.set_generate_config(config=gen_config)
        response = api.generate(prompt=messages)

        messages.append(response.model_dump())

        print(response)
        tool_name = response.tool_calls[0].function.name
        tool_params = eval(response.tool_calls[0].function.arguments)
        obs = fund_tools(tool_name=tool_name, tool_params=tool_params)
        messages.append({
            "role": "tool",
            "content": obs,
            "tool_call_id": response.tool_calls[0].id,
        })
        response = api.generate(prompt=messages)
        print(response)

    def test_agent_class(self):
        """"""
        messages = [
            UserPrompt(content='请帮我查找020532的最新信息。').model_dump(),
        ]
        fund_agent = FundAgent(verbose=True)
        fund_agent.set_llm(remote=Remote.zhipu, api_key_path=self.api_key_path, is_message_cache=True)
        out = fund_agent(prompt=messages)
        print(out)

    def test_agent_fund_basic_info(self):
        """"""
        messages = [
            UserPrompt(content='请帮我查找020532基金的基本信息。').model_dump(),
        ]
        fund_agent = FundAgent(verbose=True)
        fund_agent.set_llm(remote=Remote.zhipu, api_key_path=self.api_key_path, is_message_cache=True)
        out = fund_agent(prompt=messages)
        print(out)

    def test_agent_fund_name2code(self):
        """"""
        messages = [
            UserPrompt(content='查找湘财鑫睿债券的基金代码。').model_dump(),
        ]
        fund_agent = FundAgent(verbose=True)
        fund_agent.set_llm(remote=Remote.zhipu, api_key_path=self.api_key_path, is_message_cache=True)
        out = fund_agent(prompt=messages)
        print(out)

    def test_agent_fund_name2code_stream(self):
        """"""
        messages = [
            UserPrompt(content='查找大成消费主题的基金代码。').model_dump(),
        ]
        fund_agent = FundAgent(verbose=True, stream=True)
        fund_agent.set_llm(
            remote=Remote.zhipu,
            api_key_path=self.api_key_path,
            is_message_cache=True,
        )
        out = fund_agent(prompt=messages)
        for item in out:
            print(item)

    def test(self):
        """"""
        import sys
        from io import StringIO

        text = """print("生还者人数：", 1)"""
        stdout_backup = sys.stdout
        sys.stdout = StringIO()
        exec(text)
        output = sys.stdout.getvalue()
        sys.stdout = stdout_backup
        print("Captured output:", output)
