import torch
from ...models import app, logger


__all__ = [
    "gpu_memory_cache"
]


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
