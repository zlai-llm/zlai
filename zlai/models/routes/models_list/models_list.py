from openai.pagination import SyncPage
from zlai.models import app
from zlai.models.config.models import total_models
from zlai.types.models_list import Model


__all__ = [
    "models_list",
]


@app.get("/models")
async def models_list():
    """"""
    data = [Model(id=model_name) for model_name, _ in total_models.items()]
    _model_lst = SyncPage[Model](data=data, object='list')
    return _model_lst
