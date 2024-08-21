import os
import io
import time
import traceback
from typing import Optional, Literal
from PIL.Image import open
from fastapi import HTTPException, File, Form, UploadFile

from zlai.utils.config import pkg_config
from zlai.models.diffusers import LoadModelDiffusers
from zlai.models.utils import load_model_config
from zlai.models import app, logger
from zlai.models.config.models import diffusers_models
from zlai.types.request.image import *
from zlai.types.response.image import *


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
        models_config = load_model_config(path=models_config_path).get("models_config")
        model_config = models_config.get(request.model)
        base_config = diffusers_models.get(request.model)

        if model_config is None or base_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ImagesGenerations] Model config: {model_config}")
            base_config.update_kwargs(model_path=model_config.get("model_path"))

        generate_config = base_config.generate_method.model_validate(request.gen_kwargs())
        logger.info(f"[ImagesGenerations] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model_diffusers = LoadModelDiffusers(
                model_config=base_config, model_name=request.model,
                generate_config=generate_config, logger=logger)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")

        try:
            b64_img = model_diffusers.diffusers()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Generate Image Error: {e}")

    return ImagesResponse(created=int(time.time()), data=[Image(b64_json=b64_img, revised_prompt="b64_json")])


@app.post("/images/edits")
async def images_edits(
        image: UploadFile = File(...),
        prompt: str = Form(...),
        mask: Optional[UploadFile] = File(None),
        model: Optional[str] = Form(...),
        n: Optional[int] = 1,
        size: Optional[Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]] = "1024x1024",
        response_format: Optional[Literal["url", "b64_json"]] = "b64_json",
        user: Optional[str] = None,
):
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        logger.error(f"[ImagesGenerations] Models config path: {models_config_path} not exists.")
        raise HTTPException(status_code=404, detail="Models config path not exists.")
    else:
        image = open(io.BytesIO(image.file.read())).convert("RGB")
        request = ImagesEditsRequest(
            image=image, prompt=prompt, mask=mask, model=model,
            n=n, size=size, response_format=response_format, user=user
        )

        logger.info(f"[ImagesGenerations] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path).get("models_config")
        model_config = models_config.get(request.model)
        base_config = diffusers_models.get(request.model)

        if model_config is None or base_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ImagesGenerations] Model config: {model_config}")
            base_config.update_kwargs(model_path=model_config.get("model_path"))

        generate_config = base_config.generate_method.model_validate(request.gen_kwargs())
        logger.info(f"[ImagesGenerations] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model_diffusers = LoadModelDiffusers(
                model_config=base_config, model_name=request.model,
                generate_config=generate_config, logger=logger)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Load Model Error: {e}\n\n{traceback.format_exc()}")

        try:
            b64_img = model_diffusers.diffusers()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Generate Image Error: {e}\n\n{traceback.format_exc()}")

    return ImagesResponse(created=int(time.time()), data=[Image(b64_json=b64_img, revised_prompt="b64_json")])
