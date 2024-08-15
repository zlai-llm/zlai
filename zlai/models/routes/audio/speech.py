import os
from fastapi import HTTPException, Response
from zlai.utils import pkg_config
from zlai.models.utils import load_model_config, get_model_config

from zlai.models.types.audio import *
from ....models import app, logger


__all__ = [
    "embeddings"
]


@app.post("/audio/speech")
def embeddings(
    request: SpeechRequest
):
    """"""
    print(request)
    with open("/Users/chensy/OneDrive/代码及文档/zlai/zlai/test/test_data/audio/audio.wav", "rb") as audio:
        content = audio.read()
    response = Response(content=content, media_type="audio/wav",)
    print(response)
    return response
