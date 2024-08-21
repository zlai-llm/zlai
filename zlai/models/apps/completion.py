import os
import click
import pickle
import uvicorn
from typing import Union, Optional
from zlai.models import app
from zlai.utils.config import pkg_config
from zlai.models.config.models import chat_completion_models


__all__ = [
    "app",
    "chat_completion_model",
]


@click.command()
@click.option("--model_path", default=None, type=str, required=False)
@click.option("--model_name", default=None, type=str, required=False)
@click.option("--host", "-h", default="localhost", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--reload", "-r", default=True, type=bool, required=False, help="reload")
def chat_completion_model(
        model_path: Optional[str] = None,
        model_name: Optional[str] = None,
        host: Optional[str] = "localhost",
        port: Union[int, str] = 8000,
        reload: Union[int, bool] = True,
) -> None:
    """"""
    if model_name not in chat_completion_models:
        raise ValueError(f"model_name must be in {chat_completion_models.keys()}")

    model_config = chat_completion_models.get(model_name)
    if model_path is not None:
        model_config.model_path = model_path
    with open(os.path.join(pkg_config.cache_path, f"{model_name}_config.pkl"), 'wb') as f:
        pickle.dump(model_config, f)
    uvicorn.run("zlai.models.apps.completion:app", host=host, port=port, reload=reload, workers=1)
