from pydantic import BaseModel
from typing import Literal, Optional


__all__ = ["ImagesGenerationsRequest"]


class ImagesGenerationsRequest(BaseModel):
    """"""
    prompt: str
    """A text description of the desired image(s). The maximum length is 1000 characters for 
    dall-e-2 and 4000 characters for dall-e-3."""

    model: Optional[str] = "dall-e-2"
    """The model to use for image generation."""

    n: Optional[int] = 1
    """The number of images to generate. Must be between 1 and 10. For dall-e-3, only n=1 is supported."""

    quality: Optional[Literal["standard", "hd"]] = "standard"
    """The quality of the image that will be generated. hd creates images with finer details and greater 
    consistency across the image. This param is only supported for dall-e-3."""

    response_format: Optional[Literal["url", "b64_json"]] = "b64_json"
    """The format in which the generated images are returned. Must be one of url or b64_json. 
    URLs are only valid for 60 minutes after the image has been generated."""

    size: Optional[Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]] = "1024x1024"
    """The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024 for dall-e-2. 
    Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models."""

    style: Optional[Literal["natural", "vivid"]] = "vivid"
    """The style of the generated images. Must be one of vivid or natural. 
    Vivid causes the model to lean towards generating hyper-real and dramatic images. 
    Natural causes the model to produce more natural, less hyper-real looking images. 
    This param is only supported for dall-e-3.
    """

    user: Optional[str] = None
    """A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse."""
