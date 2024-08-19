import os
import pickle
from fastapi import HTTPException
from zlai.utils.config import pkg_config
from ...models import logger


__all__ = [
    "load_model_config",
]


def load_model_config(
        model_name: str,
        inference_name: str,
):
    """"""
    model_config_path = os.path.join(pkg_config.cache_path, f"{model_name}_config.pkl")
    if not os.path.exists(model_config_path):
        resp_content = f"[{inference_name}] Models config path: {model_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        with open(model_config_path, 'rb') as f:
            model_config = pickle.load(f)
    return model_config
