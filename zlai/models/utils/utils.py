import yaml
import time
import torch
import string
import random
from typing import List, Dict, Union, Literal, Optional
from zlai.types.completion_usage import CompletionUsage
from zlai.types.chat.chat_completion_chunk import Choice as ChunkChoice
from zlai.types.chat.chat_completion_chunk import ChoiceDelta, ChatCompletionChunk


__all__ = [
    "load_model_config",
    "get_device_max_memory",
    "stream_chunk",
    "stream_message_chunk",
    "generate_id",
    "get_model_config",
    "get_device_max_memory",
]


def get_device_max_memory(max_memory: Optional[Dict] = None) -> Dict:
    """"""
    if max_memory is None and torch.cuda.is_available():
        max_memory = {0: "20GB"}
    else:
        max_memory = None
    return max_memory


def load_model_config(path: str) -> Dict:
    """"""
    with open(path, 'r') as f:
        models_config = yaml.load(f, Loader=yaml.FullLoader)
    return models_config


def get_device_max_memory(max_memory: Optional[Dict] = None) -> Dict:
    """"""
    if max_memory is None and torch.cuda.is_available():
        max_memory = {0: "20GB"}
    else:
        max_memory = None
    return max_memory


def stream_chunk(
        _id: str, choice: ChunkChoice, model: str, usage: CompletionUsage
) -> ChatCompletionChunk:
    """"""
    chunk = ChatCompletionChunk(
        id=_id, object="chat.completion.chunk", created=int(time.time()),
        model=model, choices=[choice], usage=usage
    )
    return chunk


def stream_message_chunk(
        content: str,
        finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]],
        model: Optional[str],
        usage: Optional[CompletionUsage] = None,
        _id: Optional[str] = None,
) -> ChatCompletionChunk:
    """"""
    choice = ChunkChoice(index=0, finish_reason=finish_reason, delta=ChoiceDelta(content=content))
    chunk = stream_chunk(_id, choice, model=model, usage=usage)
    return chunk


def generate_id(prefix: str, k: int = 29) -> str:
    """"""
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return f"{prefix}{suffix}"


def get_model_config(
        model_name: str,
        models_config: List[Dict],
) -> Union[Dict, None]:
    """"""
    for config in models_config:
        if config["model_name"] == model_name:
            return config
    return None
