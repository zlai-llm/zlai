import click
import uvicorn
from typing import Union, Optional
from zlai.models import app
from zlai.models.route.chat_completion import *


__all__ = [
    "app",
    "models",
]


@click.command()
@click.option("--model_path", default=None, type=str, required=False)
@click.option("--host", "-h", default="localhost", type=str, required=False, help="host")
@click.option("--port", "-p", default=8000, type=int, required=False, help="port")
@click.option("--reload", "-r", default=True, type=bool, required=False, help="reload")
def models(
        model_path: Optional[str] = None,
        host: Optional[str] = "localhost",
        port: Union[int, str] = 8000,
        reload: Union[int, bool] = True,
) -> None:
    """"""

    uvicorn.run("zlai.models.apps.completion:app", host=host, port=port, reload=reload, workers=1)
