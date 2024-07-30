import os
import click
import shutil
import uvicorn
from typing import Union, Optional

from zlai.utils.config import pkg_config
from zlai.models import app


__all__ = [
    "app",
    "models",
]


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
    if config_path is not None:
        shutil.copy(config_path, os.path.join(pkg_config.cache_path, "models_config.yml"))
    uvicorn.run("zlai.models.app:app", host=host, port=port, reload=reload, workers=1)


if __name__ == "__main__":
    models()
