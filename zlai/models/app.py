import os
import yaml
import time
import click
import uvicorn
import shutil
from typing import List, Dict, Union, Optional
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG
from starlette.responses import StreamingResponse
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from zlai.models.types.chat_completion_chunk import *
from zlai.models.types.schema import *
from zlai.utils.config import pkg_config
from .load import *


__all__ = ["app"]

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
app = FastAPI(title="OpenAI-compatible API")


def load_model_config(path: str) -> Dict:
    """"""
    with open(path, 'r') as f:
        models_config = yaml.load(f, Loader=yaml.FullLoader)
    return models_config


@app.get("/")
def read_root():
    """"""
    return {"ZLAI": "This is open source LLM model server."}


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """"""
    models_config = load_model_config(path=os.path.join(pkg_config.cache_path, "models_config.yml"))
    models_config = models_config.get("models_config")
    model_completion = LoadModelCompletion(models_config=models_config, model_name=request.model)
    resp_content = model_completion.completion(messages=request.model_dump().get("messages"))
    if request.stream:
        return StreamingResponse(_resp_async_generator(resp_content), media_type="application/x-ndjson")
    chat_completion = ChatCompletion(
        id="1337",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                finish_reason="stop", index=0,
                message=ChatCompletionMessage(role="assistant", content=resp_content))
        ]
    )
    return chat_completion


@click.command()
@click.option("--config_path", default=None, type=str, required=False)
@click.option("--host", "-h", default="localhost", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--reload", "-r", default=True, type=bool, required=False, help="reload")
def models(
        config_path: Optional[str] = None,
        host: Optional[str] = "localhost",
        port: Union[int, str] = 8000,
        reload: Union[int, bool] = True,
) -> None:
    """"""
    if config_path is None:
        config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    else:
        shutil.copy(config_path, os.path.join(pkg_config.cache_path, "models_config.yml"))
    uvicorn.run("zlai.models.app:app", host=host, port=port, reload=reload, workers=1)


if __name__ == "__main__":
    models()
