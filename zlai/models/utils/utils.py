import yaml
import torch
from typing import List, Dict, Optional
from zlai.types import TypeMessage, ImageMessage


__all__ = [
    "load_model_config",
    "get_device_max_memory",
    "trans_messages",
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
