import torch
from zlai.models import app, logger
from zlai.models.load.chat_completion import load_method_mapping as load_completion
from zlai.models.load.diffusers import load_method_mapping as load_diffusers
from zlai.models.load.audio import load_method_mapping as load_tts
from zlai.models.load.embedding import load_method_mapping as load_embedding
from zlai.models.types.cache import DropModelRequest


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
def drop_model(request: DropModelRequest):
    """"""
    load_method = get_load_method()
    drop_methods = []
    drop_path = []
    for load_name, method in load_method.items():
        if load_name in request.method:
            method.cache.clear()
            drop_methods.append(load_name)
        if len(list(method.cache)) != 0:
            for path in request.path:
                if (path, ) in list(method.cache):
                    method.cache.pop((path, ))
                    drop_path.append(path)
    return {"method": drop_methods, "path": drop_path}
