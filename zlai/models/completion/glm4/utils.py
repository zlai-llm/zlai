from typing import List, Dict, Optional
from zlai.types.messages import *


__all__ = [
    "ChatMessage",
    "ProcessMessages",
]


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
            elif message.role in ("function", "tool"):
                message = ObservationMessage(content=message.content)
                self.processed_messages.append(message)
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
