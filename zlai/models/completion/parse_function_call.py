import re
import json
import random
import string
from typing import Any, List, Dict, Optional
from zlai.types.messages import *
from zlai.types.function_call import *
from zlai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCallFunction, ChoiceDeltaToolCall


__all__ = ["ParseFunctionCall"]


class ParseFunctionCall:

    def __init__(
            self,
            content: str,
            tools: Union[dict, List[dict]] = None,
            use_tool: Optional[bool] = True,
            special_tools: Optional[List[str]] = None,
            model: Optional[str] = None,
            tokenizer: Optional[Any] = None,
    ):
        """
        TODO 这是一个简单的工具比较函数，能保证拦截所有非工具输出的结果，需要做进一步优化
        :param output:
        :param tools:
        :param use_tool:
        """
        self.content = content
        self.tools = tools
        self.use_tool = use_tool
        self.model = model
        self.tokenizer = tokenizer
        if special_tools is None:
            self.special_tools = ["cogview", "simple_browser"]
        else:
            self.special_tools = special_tools

    def _parse_cogview(self, arguments: str) -> FunctionCall:
        """"""
        arguments = json.dumps({
            "prompt": arguments
        }, ensure_ascii=False)
        return FunctionCall(name="cogview", arguments=arguments)

    def _parse_simple_browser(self, arguments: str) -> FunctionCall:
        """"""
        search_pattern = re.compile(r'search\("(.+?)"\s*,\s*recency_days\s*=\s*(\d+)\)')
        match = search_pattern.match(arguments)
        if match:
            arguments = json.dumps({
                "query": match.group(1),
                "recency_days": int(match.group(2))
            }, ensure_ascii=False)
        return FunctionCall(name="simple_browser", arguments=arguments)

    def _parse_tool(self, function_name: str, arguments: str) -> FunctionCall:
        """"""
        try:
            arguments_json = json.loads(arguments)
        except json.JSONDecodeError:
            arguments_json = None
        arguments = json.dumps(
            arguments_json if isinstance(arguments_json, dict) else arguments,
            ensure_ascii=False)
        return FunctionCall(name=function_name, arguments=arguments)

    def _parse_min_cpm_v3(self, content: str) -> ChatCompletionMessage:
        """"""
        message = self.tokenizer.decode_function_call(content)
        return ChatCompletionMessage.model_validate(message)

    def parse(self) -> Union[str, FunctionCall, ChatCompletionMessage]:
        """"""
        if self.tools is None:
            return self.content

        if self.model == "MiniCPM3-4B":
            return self._parse_min_cpm_v3(self.content)

        lines = self.content.strip().split("\n")
        tools = {tool['function']['name'] for tool in self.tools} if self.tools else {}

        if "name" in self.content and "arguments" in self.content:
            try:
                function_json = eval(self.content)
                name = function_json.get("name")
                if name in tools:
                    return FunctionCall(name=name, arguments=str(function_json.get("arguments")))
                else:
                    return self.content
            except json.JSONDecodeError:
                pass

        elif len(lines) >= 2 and lines[1].startswith("{"):
            function_name = lines[0].strip()
            arguments = "\n".join(lines[1:]).strip()
            if self.use_tool and function_name == "simple_browser":
                function_call = self._parse_simple_browser(arguments=arguments)
            elif self.use_tool and function_name == "cogview":
                function_call = self._parse_cogview(arguments=arguments)
            elif function_name in tools:
                function_call = self._parse_tool(function_name=function_name, arguments=arguments)
            else:
                function_call = FunctionCall(name=function_name, arguments=arguments)
            return function_call

        return self.content.strip()

    def generate_id(self, prefix: str, k: int = 29) -> str:
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
        return f"{prefix}{suffix}"

    def to_chat_completion_message(self) -> ChatCompletionMessage:
        """"""
        function_call = self.parse()

        if isinstance(function_call, ChatCompletionMessage):
            return function_call

        if isinstance(function_call, FunctionCall):
            function = Function.model_validate(function_call.model_dump())
            tool_calls = [
                ChatCompletionMessageToolCall(
                    id=self.generate_id('call_', 24),
                    function=function,
                    type="function")
            ]
        else:
            tool_calls = None
        response_message = ChatCompletionMessage(
            role="assistant",
            content=None if tool_calls else self.content,
            function_call=None,
            tool_calls=tool_calls,
        )
        return response_message

    def to_stream_completion_delta(self) -> ChoiceDelta:
        """"""
        function_call = self.parse()
        if isinstance(function_call, FunctionCall):
            function = ChoiceDeltaToolCallFunction.model_validate(function_call.model_dump())
            tool_calls = [
                ChoiceDeltaToolCall(
                    index=0,
                    id=self.generate_id('call_', 24),
                    function=function,
                    type="function"
                )
            ]
        else:
            tool_calls = None
        response_message = ChoiceDelta(
            role="assistant",
            content=None if tool_calls else self.content,
            function_call=None,
            tool_calls=tool_calls,
        )
        return response_message
