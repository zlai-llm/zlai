import os
import time
from starlette.responses import StreamingResponse
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from zlai.models.types.schema import *
from zlai.utils.config import pkg_config
from ..completion import *
from ..utils import load_model_config
from ...models import app, logger


__all__ = [
    "chat_completions"
]


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """"""
    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        logger.error(f"Models config path: {models_config_path} not exists.")
        resp_content = "Error: Models config path not exists."
    else:
        logger.info(f"Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path)
        models_config = models_config.get("models_config")
        model_completion = LoadModelCompletion(
            models_config=models_config, model_name=request.model,
            generate_config=StreamInferenceGenerateConfig.model_validate(request.model_dump()),
            logger=logger)

        if request.stream:
            return StreamingResponse(
                model_completion.stream_completion(messages=request.model_dump().get("messages")),
                media_type="application/x-ndjson")
        else:
            resp_content = model_completion.completion(messages=request.model_dump().get("messages"))

    chat_completion = ChatCompletion(
        id="1337",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                finish_reason="stop", index=0,
                message=ChatCompletionMessage(role="assistant", content=resp_content))
        ]
    )
    return chat_completion
