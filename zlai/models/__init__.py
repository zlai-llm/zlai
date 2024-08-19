import logging
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG

app = FastAPI(title="OpenAI-compatible API for ZLAI")
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
