import io
import time
import traceback
from typing import Optional, Literal
from PIL.Image import open
from fastapi import HTTPException, File, Form, UploadFile

from zlai.models.diffusers import LoadModelDiffusers
from zlai.models.utils import load_model_config
from zlai.types.request.image import ImagesGenerationsRequest, ImagesEditsRequest
from zlai.types.response.image import ImagesResponse, Image
from ..utils import *
from ....models import app, logger


__all__ = [
    "images_generations"
]


@app.post("/{model_name}/images/generations")
def images_generations(
    model_name: str,
    request: ImagesGenerationsRequest
):
    """"""
    model_config = load_model_config(model_name=model_name, inference_name="ImagesGenerations")
    generate_config = model_config.generate_method.model_validate(request.model_dump())
    logger.info(f"[ImagesGenerations] Generate kwargs: {generate_config.gen_kwargs()}")

    try:
        model_diffusers = LoadModelDiffusers(
            model_config=model_config, model_name=request.model,
            generate_config=generate_config, logger=logger)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")

    try:
        b64_img = model_diffusers.diffusers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Generate Image Error: {e}")

    return ImagesResponse(created=int(time.time()), data=[Image(b64_json=b64_img, revised_prompt="b64_json")])


@app.post("{model_name}/images/edits")
async def images_edits(
        model_name: str,
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
    model_config = load_model_config(model_name=model_name, inference_name="ImagesGenerations")
    image = open(io.BytesIO(image.file.read())).convert("RGB")
    request = ImagesEditsRequest(
        image=image, prompt=prompt, mask=mask, model=model,
        n=n, size=size, response_format=response_format, user=user
    )
    generate_config = model_config.generate_method.model_validate(request.model_dump())
    logger.info(f"[ImagesGenerations] Generate kwargs: {generate_config.gen_kwargs()}")

    try:
        model_diffusers = LoadModelDiffusers(
            model_config=model_config, model_name=request.model,
            generate_config=generate_config, logger=logger)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Load Model Error: {e}\n\n{traceback.format_exc()}")

    try:
        b64_img = model_diffusers.diffusers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Generate Image Error: {e}\n\n{traceback.format_exc()}")

    return ImagesResponse(created=int(time.time()), data=[Image(b64_json=b64_img, revised_prompt="b64_json")])
