import io
import base64
from PIL import Image


__all__ = [
    "trans_bs64_to_image",
    "trans_image_to_bs64"
]


def trans_bs64_to_image(bs64: str):
    """"""
    img_bytes = base64.b64decode(bs64)
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    return image


def trans_image_to_bs64(image: Image.Image) -> str:
    """"""
    img_bytes = io.BytesIO()
    if image.mode == "RGB":
        image.save(img_bytes, format='JPEG')
    elif image.mode == "RGBA":
        image.save(img_bytes, format='PNG')
    else:
        raise ValueError("Unsupported image mode: {}".format(image.mode))
    img_bs64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return img_bs64
