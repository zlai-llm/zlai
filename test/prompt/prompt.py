import unittest
from zlai.embedding import Embedding, PretrainedEmbedding
from zlai.prompt import MessagesPrompt, PromptTemplate
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


class TestPromptTemplate(unittest.TestCase):
    """"""
    def test_template(self):
        """"""
        PROMPT_SUMMARY_TMP = """Content: {content}\nQuestion: {question}"""

        summary_prompt = PromptTemplate(
            input_variables=["content", "question"],
            template=PROMPT_SUMMARY_TMP)

        system_message = SystemMessage(
            content="""You were a helpful assistant, answering questions using the reference content provided.""")

        print(summary_prompt.format(content="1+3=", question="What is the answer?"))
        print()
        print(summary_prompt.format(content="1+3=", question="What is the answer?").to_string())
        print()
        print(summary_prompt.format(content="1+3=", question="What is the answer?").to_messages(role="user"))
        print()
        print(summary_prompt.format_prompt(content="1+3=", question="What is the answer?").to_messages(role="user"))
