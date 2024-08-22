import requests
from urllib.parse import urljoin
from typing import List, Dict, Union
from pydantic import BaseModel


__all__ = [
    "ModelCache"
]


class ModelCache(BaseModel):
    """"""
    base_url: str = "http://localhost:8000"

    def __init__(self, **data):
        super().__init__(**data)

    def list_models(self) -> list:
        """"""
        response = requests.post(urljoin(self.base_url, "/cache/list_cached_models"))
        return response.json().get("cached_models", [])

    def clear_gpu_memory(self) -> dict:
        """"""
        response = requests.post(urljoin(self.base_url, "/cache/clear_gpu_memory"))
        return response.json()

    def clear_model_cache(self, model_name: Union[str, List[str]]) -> Dict:
        """"""
        url = urljoin(self.base_url, "/cache/clear_model_cache")
        response = requests.post(url, json={"model_name": model_name})
        return response.json()

    def gpu_memory(self, device: Union[int, List[int]] = 0) -> dict:
        """"""
        url = urljoin(self.base_url, "/cache/gpu_memory")
        response = requests.post(url, json={"device": device})
        return response.json()
