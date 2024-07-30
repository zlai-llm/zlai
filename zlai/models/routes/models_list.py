from openai.pagination import SyncPage
from ...models import app
from ..types.model_list import *


__all__ = [
    "models_list",
]


@app.get("/models")
async def models_list():
    """"""
    data = [Model(id=model_name) for model_key, model_name in _model_list.model_dump().items()]
    _model_lst = SyncPage[Model](data=data,object='list')
    return _model_lst
