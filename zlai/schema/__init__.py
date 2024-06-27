from typing import Union

from .url import *
from .messages import *
from .models import *
from .response import *
from .request import *
from .document import *
from .output import *
from .schema import *

MessageType = Union[Message, UserMessage, AssistantMessage, ImagePrompt, ToolsMessage, CompletionMessage]
