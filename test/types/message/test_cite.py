import unittest
from zlai.types.messages import CiteMessage


class TestCite(unittest.TestCase):
    def test_cite(self):
        """"""
        message = CiteMessage(query="b", cite="a")
        print(message)
        print(message.to_dict())
        print(CiteMessage.model_validate(message.to_dict()))