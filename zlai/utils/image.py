import io
import base64
from PIL import Image


__all__ = [
    "trans_bs64_to_image"
]


def trans_bs64_to_image(bs64: str):
    """"""
    img_bytes = base64.b64decode(bs64)
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    return image
