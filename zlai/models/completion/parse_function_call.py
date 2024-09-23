from typing import Any, List, Dict, Callable, Optional
from zlai.types.messages import *
from zlai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCallFunction, ChoiceDeltaToolCall
from zlai.parse.function_call import *


__all__ = ["ParseFunctionCall"]


class ParseFunctionCall:

    def __init__(
            self,
            content: str,
            tools: Union[dict, List[dict]] = None,
            tokenizer: Optional[Any] = None,
            parse_func: Optional[Callable] = None,
            stream: bool = False,
            **kwargs: Any,
    ):
        """
        TODO 这是一个简单的工具比较函数，能保证拦截所有非工具输出的结果，需要做进一步优化
        :param output:
        :param tools:
        :param use_tool:
        """
        self.content = content
        self.tools = tools
        self.parse_func = parse_func
        self.tokenizer = tokenizer
        self.stream = stream
        self.kwargs = kwargs
        self._tools_name()

    def _tools_name(self):
        """"""
        self.tools_name = {tool['function']['name'] for tool in self.tools} if self.tools else {}

    def parse(self) -> Optional[List[Dict]]:
        """"""
        if self.tools is None:
            return None
        else:
            functions = self.parse_func(content=self.content, tools_name=self.tools_name, tokenizer=self.tokenizer)
            return functions

    def to_message_instance(self) -> Union[ChatCompletionMessage, ChoiceDelta]:
        """"""
        functions = self.parse()
        return message_instance(content=self.content, functions=functions, stream=self.stream)
