import unittest
from zlai.llms import Zhipu, GLM4GenerateConfig, GLM4FlashGenerateConfig
from zlai.agent.tools import *


class TestToolsAgent(unittest.TestCase):
    """"""

    def test_tools_agent(self):
        """"""
        llm = Zhipu(generate_config=GLM4FlashGenerateConfig())

        tools = Tools(function_list=[get_weather, random_number_generator])
        agent = ToolsAgent(llm=llm, tools=tools, verbose=True)
        task_completion = agent("输出一个0-6的随机数？")
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
