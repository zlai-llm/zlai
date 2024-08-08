import os
from fastapi import HTTPException
from starlette.responses import StreamingResponse
from typing import List, Dict, Union
from zlai.models.types.schema import *
from zlai.utils.config import pkg_config
from zlai.models.types.images_generations import *
from zlai.models.diffusers import LoadModelDiffusers
from zlai.models.utils import load_model_config, get_model_config
from ...completion import *
from ....models import app, logger


__all__ = [
    "images_generations"
]


@app.post("/images/generations")
def images_generations(
    request: ImagesGenerationsRequest
):
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        logger.error(f"[ChatCompletion] Models config path: {models_config_path} not exists.")
        raise HTTPException(status_code=404, detail="Models config path not exists.")
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

    #     tools_config = ToolsConfig.model_validate(request.model_dump())
    #     generate_config = model_config.generate_method.model_validate(request.model_dump())
    #     logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")
    #
    #     try:
    #         model_completion = LoadModelCompletion(
    #             models_config=models_config, model_name=request.model,
    #             generate_config=generate_config, tools_config=tools_config,
    #             logger=logger)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")
    #
    #     if request.stream:
    #         return StreamingResponse(
    #             model_completion.stream_completion(messages=request.messages),
    #             media_type="application/x-ndjson")
    #     else:
    #         return model_completion.completion(messages=request.messages)
    #
    #
    # logger.info(msg=request)
    # return ImagesResponse(created=12, data=[Image(b64_json="dadas", url="https://www.baidu.com", revised_prompt="b64_json")])
