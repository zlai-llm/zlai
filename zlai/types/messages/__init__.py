from typing import Union
from .audio import *
from .base import *
from .function import *
from .image import *
from .messages import *


TypeMessage = Union[
    Message,
    ChatMessage,
    SystemMessage,
    SystemToolsMessage,
    UserMessage,
    AssistantMessage,
    AssistantWithMetadataMessage,
    ObservationMessage,
    FunctionMessage,
    ToolMessage,
    ToolsMessage,
    ImageMessage,
    AudioMessage,
    ChatCompletionMessage,
]
