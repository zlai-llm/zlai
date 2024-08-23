from typing import Union
from .audio import *
from .base import *
from .chart import *
from .function import *
from .image import *
from .messages import *
from .table import *


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
    ChartMessage,
    TableMessage,
]
