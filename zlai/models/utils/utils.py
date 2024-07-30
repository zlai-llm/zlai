import yaml
from typing import Dict


__all__ = [
    "load_model_config"
]


def load_model_config(path: str) -> Dict:
    """"""
    with open(path, 'r') as f:
        models_config = yaml.load(f, Loader=yaml.FullLoader)
    return models_config
