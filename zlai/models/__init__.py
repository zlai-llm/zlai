# from .app import *
# from zlai.models.types.schema import *
# from zlai.models.types.chat_completion_chunk import *
import logging
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG

app = FastAPI(title="OpenAI-compatible API for ZLAI")
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

from zlai.models.app import *
from zlai.models.routes import *


# todo: 增加 API-embedding 的接口
# todo: 增加 GLM-stream
# todo: 增加 GLM-FunctionCall-stream
