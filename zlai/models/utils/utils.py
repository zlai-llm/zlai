import yaml
import time
import torch
import string
import random
from typing import List, Dict, Literal, Optional
from zlai.types import TypeMessage, ImageMessage
from zlai.types.chat_completion_chunk import Choice as ChunkChoice
from zlai.types.chat_completion_chunk import ChoiceDelta, ChatCompletionChunk


__all__ = [
    "load_model_config",
    "get_device_max_memory",
    "trans_messages",
    "stream_chunk",
    "stream_message_chunk",
    "generate_id",
]


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


def trans_messages(messages: List[TypeMessage]) -> List[Dict]:
    """"""
    _messages = []
    image_idx = []
    for i, message in enumerate(messages):
        if isinstance(message, ImageMessage):
            message.split_image()
            image_idx.append(i)
        _messages.append(message.model_dump())
    if len(image_idx) > 1:
        for _id in image_idx[:-1]:
            _ = _messages[_id].pop("image")
    return _messages


def stream_chunk(_id: str, choice: ChunkChoice, model: str) -> ChatCompletionChunk:
    """"""
    chunk = ChatCompletionChunk(
        id=_id, object="chat.completion.chunk", created=int(time.time()),
        model=model, choices=[choice],
    )
    return chunk


def stream_message_chunk(
        content: str,
        finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]],
        model: Optional[str],
        _id: Optional[str],
) -> ChatCompletionChunk:
    """"""
    choice = ChunkChoice(index=0, finish_reason=finish_reason, delta=ChoiceDelta(content=content))
    chunk = stream_chunk(_id, choice, model=model)
    return chunk


def generate_id(prefix: str, k: int = 29) -> str:
    """"""
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return f"{prefix}{suffix}"
