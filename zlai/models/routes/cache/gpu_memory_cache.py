import torch
from zlai.models import app, logger
from zlai.types.cache import DropModelRequest
from zlai.models.config.models import total_models


__all__ = [
    "clear_gpu_memory",
    "list_cached_models",
    "clear_model_cache",
]


def clear_gpu_cache():
    """"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


@app.post("/cache/list_cached_models")
def list_cached_models():
    """"""
    cached_models = []
    for model_name, model_config in total_models.items():
        if len(list(model_config.load_method.cache)) != 0:
            cached_models.append(model_name)
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
            total_models.get("model").load_method.cache.clear()
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
