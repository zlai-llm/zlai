import torch
import base64
from io import BytesIO
from typing import Any, Union
from zlai.models.types.images_generations import ImageGenerateConfig, KolorsImageGenerateConfig


__all__ = [
    "kolors_generation"
]


def kolors_generation(
        pipe: Any,
        generate_config: Union[ImageGenerateConfig, KolorsImageGenerateConfig],
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
