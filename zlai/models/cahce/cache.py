import os
import requests
from typing import List, Dict, Union
from pydantic import BaseModel


__all__ = [
    "ModelCache"
]


class ModelCache(BaseModel):
    """"""
    base_url = "http://localhost:8000"

    def __init__(self, **data):
        super().__init__(**data)

    def list_models(self) -> list:
        """"""
        response = requests.get(os.path.join(self.base_url, "/cache/list_cached_models"))
        return response.json().get("cached_models", [])

    def clear_gpu_memory(self) -> dict:
        """"""
        response = requests.get(os.path.join(self.base_url, "/cache/clear_gpu_memory"))
        return response.json()

    def clear_model_cache(self, model_name: Union[str, List[str]]) -> Dict:
        """"""
        url = os.path.join(self.base_url, "/cache/clear_model_cache")
        response = requests.get(url, json={"model_name": model_name})
        return response.json()
