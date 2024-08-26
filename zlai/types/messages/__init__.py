from typing import Union
from .audio import *
from .base import *
from .chart import *
from .completion import *
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

# todo: 要增加不同的message类型组别，区分request类型与展示类型
