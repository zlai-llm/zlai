import os
import time
from fastapi import HTTPException
from zlai.models.types.schema import *
from zlai.utils.config import pkg_config
from zlai.models.types.images_generations import *
from zlai.models.diffusers import LoadModelDiffusers
from zlai.models.utils import load_model_config, get_model_config
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
        logger.error(f"[ImagesGenerations] Models config path: {models_config_path} not exists.")
        raise HTTPException(status_code=404, detail="Models config path not exists.")
    else:
        logger.info(f"[ImagesGenerations] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path)
        models_config = models_config.get("models_config")
        model_config = get_model_config(model_name=request.model, models_config=models_config)

        if model_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ImagesGenerations] Model config: {model_config}")
            model_config = ModelConfig.model_validate(model_config)

        generate_config = model_config.generate_method.model_validate(request.model_dump())
        logger.info(f"[ImagesGenerations] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model_diffusers = LoadModelDiffusers(
                models_config=models_config, model_name=request.model,
                generate_config=generate_config, logger=logger)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")

        try:
            b64_img = model_diffusers.diffusers()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Generate Image Error: {e}")

    return ImagesResponse(created=int(time.time()), data=[Image(b64_json=b64_img, revised_prompt="b64_json")])
