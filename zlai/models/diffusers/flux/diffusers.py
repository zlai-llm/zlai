import torch
import base64
from io import BytesIO
from typing import Any
from zlai.types.generate_config.image import *


__all__ = [
    "flux_generation",
]


def flux_generation(
        pipe: Any,
        generate_config: Union[ImageGenerateConfig, KolorsImageGenerateConfig],
        **kwargs: Any,
) -> str:
    """Generate image using FLUX Diffusers model."""
    image = pipe(
        **generate_config.gen_kwargs(),
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator(pipe.device).manual_seed(0)
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64
