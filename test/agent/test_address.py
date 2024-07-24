import unittest
from zlai.llms import *
from zlai.agent import *


class TestAddressAgent(unittest.TestCase):
    """"""
    def setUp(self):
        """"""
        self.llm = Zhipu(generate_config=GLM4GenerateConfig())

    def test_address_agent(self):
        """"""
        address = AddressAgent(llm=self.llm, verbose=True)
        # query = "杭州市余杭区是怎样的一个地方"
        query = "杭州今天天气怎么样？"
        answer = address(query=query)
        print(answer)
