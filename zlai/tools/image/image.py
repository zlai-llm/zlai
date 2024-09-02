import os
from PIL.Image import Image
from typing import Annotated
from zlai.utils.image import trans_bs64_to_image
from openai import OpenAI


__all__ = ["generate_image"]


def generate_image(
        prompt: Annotated[str, "生成图片的提示或者描述", True],
) -> Image:
    """
    生成图片的函数方法，给定生成图片的提示或者描述返回一张图片。
    :param prompt:
    :return:
    """
    client = OpenAI(api_key="a", base_url=os.getenv("BASE_URL", "http://localhost:8000/"))
    respose = client.images.generate(
        model="Kolors-diffusers",
        prompt=prompt,
        size="1792x1024",
        response_format="b64_json",
    )
    image = trans_bs64_to_image(respose.data[0].b64_json)
    return image
