import torch
from typing import Union, List
from zlai.models import app, logger
from zlai.models.completion.load import load_method_mapping as load_completion
from zlai.models.diffusers.load_model import load_method_mapping as load_diffusers
from zlai.models.embedding.load_model import load_method_mapping as load_embedding
from zlai.models.tts.load_model import load_method_mapping as load_tts


__all__ = [
    "gpu_memory_cache",
    "current_models",
    "drop_model",
]


def get_load_method():
    """"""
    load_method = {
        **load_completion,
        **load_diffusers,
        **load_embedding,
        **load_tts,
    }
    return load_method


@app.post("/cache/clear_gpu_memory")
def gpu_memory_cache():
    """
    Clear GPU memory cache
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    logger.info("GPU memory cache cleared.")
    return {"message": "GPU memory cache cleared."}


@app.post("/cache/current_models")
def current_models():
    """"""
    load_method = get_load_method()
    exits_models = []
    for load_name, method in load_method.items():
        exits_models.append({"load_name": load_name, "cache": list(method.cache)})
    return exits_models


@app.post("/cache/drop_model")
def drop_model(name: Union[str, List[str]]):
    """"""
    if isinstance(name, str):
        name = [name]
    load_method = get_load_method()
    for load_name, method in load_method.items():
        if load_name in name:
            method.cache.clear()
            return {"message": f"Drop model <{load_name}: {list(method)}> cache success."}
    return {"message": f"Not find model: {name}"}
