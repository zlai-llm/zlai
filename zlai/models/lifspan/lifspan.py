import torch
from fastapi import FastAPI
from contextlib import asynccontextmanager
from zlai.models.completion import load_glm4


__all__ = ["startup", "shutdown"]


@asynccontextmanager
async def startup(app: FastAPI):
    """"""
    load_glm4(model_path="")
    print("load")
    yield


@asynccontextmanager
async def shutdown(app: FastAPI):
    """"""
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
