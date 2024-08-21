import torch
import base64
from io import BytesIO
from typing import Any
from zlai.types.generate_config.image import *


__all__ = [
    "kolors_generation",
    "kolors_img2img_generation"
]


def kolors_generation(
        pipe: Any,
        generate_config: Union[ImageGenerateConfig, KolorsImageGenerateConfig],
        **kwargs: Any,
) -> str:
    image = pipe(
        **generate_config.gen_kwargs(),
        negative_prompt="",
        guidance_scale=5.0,
        num_inference_steps=50,
        generator=torch.Generator(pipe.device).manual_seed(66),
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64


def kolors_img2img_generation(
        pipe: Any,
        generate_config: Union[ImageGenerateConfig, KolorsImage2ImageGenerateConfig],
        **kwargs: Any,
):
    image = pipe(**generate_config.gen_kwargs(),).images[0]
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64
