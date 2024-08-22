import torch
from typing import Tuple
from zlai.models import app, logger
from zlai.types.cache import DropModelRequest, GPUMemoryRequest
from zlai.models.config.models import total_models


__all__ = [
    "gpu_memory",
    "clear_gpu_memory",
    "list_cached_models",
    "clear_model_cache",
]


def get_gpu_memory_data(device: int) -> Tuple[float, float]:
    """"""
    data = torch.cuda.mem_get_info(device=device)
    free, total = [round(d/1024**3, 2) for d in data]
    return free, total


def clear_gpu_cache():
    """"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


@app.post("/cache/list_cached_models")
async def list_cached_models():
    """"""
    cached_models = []
    for model_name, model_config in total_models.items():
        if len(list(model_config.load_method.cache)) != 0:
            cached_params = list(model_config.load_method.cache)
            cached_models.extend([model_name for param in cached_params if model_name in param[0]])
    return {"cached_models": cached_models}


@app.post("/cache/clear_model_cache")
def clear_model_cache(request: DropModelRequest):
    """"""
    if isinstance(request.model_name, str):
        models = [request.model_name]
    else:
        models = request.model_name
    msg = []
    for model in models:
        if model in total_models:
            cache_function = total_models.get(model).load_method
            for _cache_params in list(cache_function.cache):
                if model in _cache_params[0]:
                    cache_function.cache.pop(_cache_params)
                    msg.append(f"Model {model} cache cleared.")
        else:
            msg.append(f"Model {model} not found.")
    clear_gpu_cache()
    return {"msg": msg}


@app.post("/cache/clear_gpu_memory")
def clear_gpu_memory():
    """
    Clear GPU memory cache
    """
    cleared_models = []
    for model_name, model_config in total_models.items():
        if len(list(model_config.load_method.cache)) != 0:
            model_config.load_method.cache.clear()
            cleared_models.append(model_name)
    clear_gpu_cache()
    logger.info("GPU memory cache cleared.")
    return {"message": "GPU memory cache cleared.", "cleared_models": cleared_models}


@app.post("/cache/gpu_memory")
def gpu_memory(request: GPUMemoryRequest):
    """"""
    if isinstance(request.device, int):
        devices = [request.device]
    else:
        devices = request.device

    device_data = {}
    for device in devices:
        free, total = get_gpu_memory_data(device=device)
        device_data.update({device: {"free": free, "total": total, "percent": round(free / total * 100, 2)}})
    return device_data
