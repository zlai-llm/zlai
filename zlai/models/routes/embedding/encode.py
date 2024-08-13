import os
from fastapi import HTTPException
from typing import List
from zlai.utils import pkg_config
from zlai.models.utils import load_model_config, get_model_config
from zlai.models.types import ModelConfig, ToolsConfig
from zlai.models.types.embedding import *
from ....models import app, logger


__all__ = [
    "embeddings"
]


def trans_embedding_response(vectors: List[List[float]], response: CreateEmbeddingResponse):
    """"""



@app.post("/embeddings")
def embeddings(
    request: EmbeddingRequest
) -> CreateEmbeddingResponse:
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        resp_content = f"[ChatCompletion] Models config path: {models_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        logger.info(f"[ChatCompletion] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path)
        models_config = models_config.get("models_config")
        model_config = get_model_config(model_name=request.model, models_config=models_config)

        if model_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ChatCompletion] Model config: {model_config}")
            model_config = ModelConfig.model_validate(model_config)

        tools_config = ToolsConfig.model_validate(request.model_dump())
        generate_config = model_config.generate_method.model_validate(request.model_dump())
        logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model_completion = LoadModelCompletion(
                models_config=models_config, model_name=request.model,
                generate_config=generate_config, tools_config=tools_config,
                logger=logger)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")

    response = CreateEmbeddingResponse(model=request.model)
    return response
