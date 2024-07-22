import unittest
from pydantic import BaseModel, Field, ConfigDict
from langchain.prompts import PromptTemplate
from typing import Any, Optional
from zlai.schema import *
from zlai.llms import TypeLLM, Zhipu, GLM4AirGenerateConfig
from zlai.embedding import TypeEmbedding


class TestQuickStar(unittest.TestCase):
    def test_quick_star(self):
        """"""
        messages = [
            SystemMessage(content="你是一个人工智能助手。用于记录我的日常事务。"),
            UserMessage(content="你好，我的好朋友六子昨天早晨吃了2碗粉。"),
            AssistantMessage(content="好的，我记住了。")
        ]

        llm = Zhipu(generate_config=GLM4AirGenerateConfig())

        # 新的问题
        messages.append(UserMessage(content="请问，昨天六子早上吃了几碗粉？"))
        completion = llm.generate(messages=messages)
        print(completion.choices[0].message.content)

    def test_agent(self):
        """"""
        from zlai.agent import ChatAgent, TaskDescription

        task_chat = TaskDescription(
            task=ChatAgent, task_name="聊天机器人",
            task_description="""提供普通对话聊天，不涉及专业知识与即时讯息。""",
        )
        print(task_chat)

    def test_params(self):
        """"""

        class TaskParametersV2(BaseModel):
            """"""
            model_config = ConfigDict(arbitrary_types_allowed=True)
            # model
            llm: TypeLLM = Field(default=None)
            embedding: Optional[TypeEmbedding] = Field(default=None)

            # database
            db: Optional[Any] = Field(default=None)
            db_path: Optional[str] = Field(default=None)

            # messages
            system_message: Optional[SystemMessage] = Field(default=None)
            system_template: Optional[PromptTemplate] = Field(default=None)
            prompt_template: Optional[PromptTemplate] = Field(default=None)
            # few_shot: Optional[List[Message]] = Field(default=None)
            # messages_prompt: Optional[MessagesPrompt] = Field(default=None)
            # use_memory: Optional[bool] = Field(default=False)
            # max_memory_messages: Optional[int] = Field(default=None)

            # # logger
            # logger: Optional[Callable] = Field(default=None)
            # verbose: Optional[bool] = Field(default=None)
            #
            # # ElasticSearch
            # index_name: Optional[str] = Field(default=None)
            # elasticsearch_host: Optional[str] = Field(default=None)
            #
            # # tools
            # hooks: Optional[Dict[str, Callable]] = Field(default=None)
            # tools_description: Optional[List] = Field(default=None)
            # tools_params_fun: Optional[Callable] = Field(default=None)
            #
            # kwargs: Optional[Dict] = Field(default=None)

        param = TaskParametersV2()
