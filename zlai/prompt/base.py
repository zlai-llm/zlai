from typing import Any, List, Literal, Callable, Optional
from langchain.prompts import PromptTemplate
from ..utils.mixin import *
from ..schema.messages import Message, SystemMessage, UserMessage
from ..embedding import TypeEmbedding


__all__ = [
    "MessagesPrompt",
]


class MessagesPrompt(LoggerMixin):
    """"""
    system_message: SystemMessage
    embedding: TypeEmbedding
    few_shot: List[Message]
    rerank: bool = False
    n_shot: Optional[int]
    support_system: bool
    warp_user: bool
    prompt_template: Optional[PromptTemplate]
    verbose: Optional[bool]
    logger: Optional[Callable]

    def __init__(
            self,
            system_message: SystemMessage,
            few_shot: List[Message],
            embedding: Optional[TypeEmbedding] = None,
            rerank: bool = False,
            n_shot: Optional[int] = 5,
            support_system: bool = True,
            warp_user: bool = False,
            prompt_template: Optional[PromptTemplate] = None,
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            *args, **kwargs
    ):
        """

        :param system_message:
        :param embedding:
        :param few_shot:
        :param rerank: 是否进行 few-shot 重排
        :param n_shot: 取 n 个样例
        :param support_system: 支持一些不支持消息系统机制的模型
        """
        self.system_message = system_message
        self.embedding = embedding
        self.few_shot = few_shot
        self.rerank = rerank
        self.n_shot = n_shot
        self.support_system = support_system
        self.warp_user = warp_user
        self.prompt_template = prompt_template

        self.verbose = verbose
        self.logger = logger

        # validate params
        self.validate_embedding()

    def validate_embedding(self):
        """"""
        if self.rerank and self.embedding is None:
            raise ValueError("Embedding is not provided.")

    @classmethod
    def warp_user_content(cls, messages: List[Message]) -> List[Message]:
        """"""
        new_prompt = []
        for message in messages:
            if message.role == 'user':
                message.content = f"<文本>\n{message.content}\n</文本>\n答案："
            new_prompt.append(message)
        return new_prompt

    @classmethod
    def instruct_content(cls, system_content: str, user_content: str) -> str:
        """"""
        content = f"<instruction>\n{system_content}\n</instruction>\n\n<content>{user_content}</content>"
        return content

    def validate_few_shot(self):
        """ 验证few-shot是否有效 """
        if len(self.few_shot) % 2 != 0:
            raise ValueError("Few-shot prompts must be in pairs.")
        else:
            return True

    def rerank_few_shot(
            self,
            content: str,
    ) -> List[Message]:
        """
        
        :param content:
        :return:
        """
        user_content = [message.content for message in self.few_shot if message.role == 'user']
        idx = self.embedding.match_idx(source=[content], target=user_content, top_n=self.n_shot)

        new_shot = []
        for i in idx[0][::-1]:
            new_shot.append(self.few_shot[i * 2])
            new_shot.append(self.few_shot[i * 2 + 1])
        return new_shot

    def prompt_format(
            self,
            content: Optional[str] = None,
            instruct: Literal["all", "first"] = "first",
            *args: Any,
            **kwargs: Any,
    ) -> List[Message]:
        """"""
        messages = []

        if self.prompt_template:
            kwargs.update({"content": content})
            content = self.prompt_template.format_prompt(**kwargs).to_string()

        # add system prompt
        if self.support_system and self.system_message:
            messages.append(self.system_message)

        # few shot
        if len(self.few_shot) > 0:
            if self.rerank:
                few_shot = self.rerank_few_shot(content=content)
                self._logger(msg=f"Reranked few-shot prompts: {int(len(few_shot) / 2)}")
            else:
                few_shot = self.few_shot

            for i, message in enumerate(few_shot):
                if not self.support_system:
                    if message.role == 'user' and i == 0 and instruct in ["all", "first"]:
                        message.content = self.instruct_content(
                            system_content=self.system_message.content, user_content=message.content)
                    elif message.role == 'user' and instruct == "all":
                        message.content = self.instruct_content(
                            system_content=self.system_message.content, user_content=message.content)
                messages.append(message)

        # current content
        if self.system_message and not self.support_system and instruct == 'all':
            content = self.instruct_content(system_content=self.system_message.content, user_content=content)
        messages.append(UserMessage(content=content))

        if self.warp_user:
            messages = self.warp_user_content(messages=messages)

        return messages
