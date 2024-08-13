import os
from fastapi import HTTPException
from zlai.utils import pkg_config
from zlai.models.utils import load_model_config, get_model_config
from zlai.models.embedding import LoadModelEmbedding
from zlai.models.types.embedding import *
from ....models import app, logger


__all__ = [
    "embeddings"
]


@app.post("/embeddings")
def embeddings(
    request: EmbeddingRequest
) -> CreateEmbeddingResponse:
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        resp_content = f"[Embedding] Models config path: {models_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        logger.info(f"[Embedding] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path)
        models_config = models_config.get("models_config")
        model_config = get_model_config(model_name=request.model, models_config=models_config)
        if model_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[Embedding] Model config: {model_config}")
        try:
            model_embedding = LoadModelEmbedding(
                models_config=models_config, model_name=request.model, logger=logger)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")
        try:
            response = model_embedding.encode(request.input)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Embedding Error: {e}")
    return response
