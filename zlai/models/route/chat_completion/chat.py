import os
import pickle
from fastapi import HTTPException
from starlette.responses import StreamingResponse
from zlai.models.types.models_config import *
from zlai.models.types.completion import *
from zlai.utils.config import pkg_config
from ...completion import *
from ....models import app, logger


__all__ = [
    "chat_completions"
]


@app.post("/{model_name}/chat/completions")
async def chat_completions(model_name: str, request: ChatCompletionRequest):
    """"""
    model_config_path = os.path.join(pkg_config.cache_path, f"{model_name}_config.pkl")
    if not os.path.exists(model_config_path):
        resp_content = f"[ChatCompletion] Models config path: {model_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        with open(model_config_path, 'rb') as f:
            model_config = pickle.load(f)

    if len(request.messages) < 1 or request.messages[-1].role == "assistant":
        raise HTTPException(status_code=400, detail="Invalid request, last message role must be user.")

    tools_config = ToolsConfig.model_validate(request.model_dump())
    generate_config = model_config.generate_method.model_validate(request.model_dump())
    logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")

    try:
        model_completion = LoadModelCompletion(
            model_config=model_config, model_name=request.model,
            generate_config=generate_config, tools_config=tools_config,
            logger=logger)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Load Model Error: {e}")

    if request.stream:
        return StreamingResponse(
            model_completion.stream_completion(messages=request.messages),
            media_type="application/x-ndjson")
    else:
        return model_completion.completion(messages=request.messages)
