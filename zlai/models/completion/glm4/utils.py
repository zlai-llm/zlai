import re
import json
import random
import string
from typing import List, Dict, Union, Optional
from zlai.types.messages import *
from zlai.types.function_call import *
from zlai.types.chat_completion_chunk import ChoiceDelta, ChoiceDeltaToolCallFunction, ChoiceDeltaToolCall


__all__ = [
    "ChatMessage",
    "ParseFunctionCall",
    "ProcessMessages",
]


class ParseFunctionCall:

    def __init__(
            self,
            content: str,
            tools: Union[dict, List[dict]] = None,
            use_tool: Optional[bool] = True,
            special_tools: Optional[List[str]] = None,
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

    def parse(self) -> Union[str, FunctionCall]:
        """"""
        if self.tools is None:
            return self.content

        lines = self.content.strip().split("\n")
        tools = {tool['function']['name'] for tool in self.tools} if self.tools else {}

        if len(lines) >= 2 and lines[1].startswith("{"):
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


class ProcessMessages:
    """"""
    processed_messages: List[TypeMessage]

    def __init__(
            self,
            messages: List[TypeMessage],
            tools: Optional[List[Dict]] = None,
            tool_choice: Optional[Union[dict, str]] = "none"
    ):
        self.messages = messages
        self.tools = tools
        self.tool_choice = tool_choice
        self.processed_messages = []
        self._validate_messages()
        self.process()

    def _validate_messages(self):
        """"""
        if len(self.messages) == 0:
            raise ValueError("messages must be a non-empty list")

    def filter_tools(self, tools: List[Dict], tool_choice: Union[dict, str]) -> List[Dict]:
        """"""
        if isinstance(tool_choice, dict):
            function_name = tool_choice.get('function', {}).get('name', None)
            if not function_name:
                return []
            filtered_tools = [
                tool for tool in tools
                if tool.get('function', {}).get('name') == function_name
            ]
            return filtered_tools
        else:
            return tools

    def _add_system_and_tools(self, ):
        """"""
        if self.messages[0].role == "system":
            system_message = self.messages.pop(0)
            origin_system_content = system_message.content
        else:
            origin_system_content = ""

        if self.tool_choice != "none":
            tools = self.filter_tools(tools=self.tools, tool_choice=self.tool_choice)
            new_system_message = SystemToolsMessage(content=origin_system_content, tools=tools)
            if new_system_message.content or new_system_message.tools:
                self.processed_messages.append(new_system_message)
        else:
            new_system_message = SystemMessage(content=origin_system_content)
            if new_system_message.content:
                self.processed_messages.append(new_system_message)

        if isinstance(self.tool_choice, dict) and self.tools:
            self.processed_messages.append(
                AssistantWithMetadataMessage(
                    metadata=self.tool_choice["function"]["name"],
                )
            )

    def process(self):
        """"""
        self._add_system_and_tools()
        for message in self.messages:
            if isinstance(message, ImageMessage):
                self.processed_messages.append(message)
            elif message.role == "function":
                self.processed_messages.append(FunctionMessage(content=message.content))
            elif message.role == "tool":
                self.processed_messages.append(ToolMessage(content=message.content))
            elif message.role == "assistant":
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        self.processed_messages.append(
                            AssistantWithMetadataMessage(
                                metadata=tool_call.function.name,
                                content=tool_call.function.arguments,
                            )
                        )
                else:
                    self.processed_messages.append(
                        AssistantWithMetadataMessage(content=message.content))
            else:
                self.processed_messages.append(Message.model_validate(message.model_dump()))
        return self.processed_messages

    def to_messages(self) -> List[TypeMessage]:
        """"""
        return self.processed_messages

    def to_dict(self) -> List[Dict]:
        """"""
        return [item.model_dump() for item in self.processed_messages]
