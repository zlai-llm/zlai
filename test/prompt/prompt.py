import unittest
from zlai.embedding import Embedding, PretrainedEmbedding
from zlai.prompt import MessagesPrompt
from zlai.schema import SystemMessage, UserMessage, AssistantMessage


class TestPromptFewShotRerank(unittest.TestCase):
    """"""

    def setUp(self):
        """"""

        self.system_message = SystemMessage(content="你是一个计算器")
        self.few_shot = [
            UserMessage(content="1+1="),
            AssistantMessage(content="2"),
            UserMessage(content="1+2="),
            AssistantMessage(content="3"),
            UserMessage(content="1+3="),
            AssistantMessage(content="4"),
        ]
        self.embedding = PretrainedEmbedding(model_path=...)

    def test_rerank(self):
        """"""
        messages_prompt = MessagesPrompt(
            system_message=self.system_message,
            few_shot=self.few_shot,
            n_shot=2, rerank=True,
            support_system=True,
            embedding=self.embedding,
            verbose=True,
        )
        messages = messages_prompt.prompt_format(content="1+3=")
        for message in messages:
            print(f"{message.role}: {message.content}")
