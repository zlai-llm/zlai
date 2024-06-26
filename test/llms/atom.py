import unittest
from zlai.llms import Atom
from zlai.llms.generate_config.atom import *


class TestAtom(unittest.TestCase):
    """"""
    def test_atom(self):
        """"""
        config = Atom1BGenerateConfig()
        llm = Atom(generate_config=config)
        out = llm.generate(query="你好")
        print(out)

    def test_atom_message(self):
        """"""
        config = Atom1BGenerateConfig()
        llm = Atom(generate_config=config, output="message")
        out = llm.generate(query="你好")
        print(out)

    def test_atom_str(self):
        """"""
        llm = Atom(generate_config=Atom1BGenerateConfig(), output="str")
        out = llm.generate(query="你好")
        print(out)

    def test_atom_stream(self):
        """"""
        config = Atom1BGenerateConfig(stream=True)
        llm = Atom(generate_config=config)
        out = llm.generate(query="你好")
        for o in out:
            print(o)

    def test_atom_stream_message(self):
        """"""
        config = Atom1BGenerateConfig(stream=True)
        llm = Atom(generate_config=config, output="message")
        out = llm.generate(query="你好")
        for o in out:
            print(o)

    def test_atom_stream_str(self):
        """"""
        config = Atom1BGenerateConfig(stream=True)
        llm = Atom(generate_config=config, output="str")
        out = llm.generate(query="你好")
        for o in out:
            print(o)

    def test_llama3(self):
        """"""
        config = Llama3Chinese8BInstruct()
        llm = Atom(generate_config=config)
        out = llm.generate(query="你好，介绍自己")
        print(out)
