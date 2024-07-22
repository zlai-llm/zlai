from typing import Union

try:
    from openai.types.chat import ChatCompletionMessage
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install openai")

from .url import *
from .messages import *
from .response import *
from .document import *
from .output import *
from .schema import *

TypeMessage = Union[
    Message, UserMessage, AssistantMessage, ImagePrompt, ToolsMessage, CompletionMessage, ChatCompletionMessage]
