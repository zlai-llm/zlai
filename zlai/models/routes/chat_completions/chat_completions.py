import os
from fastapi import HTTPException
from starlette.responses import StreamingResponse
from zlai.utils.config import pkg_config
from zlai.models.utils import load_model_config
from zlai.models.completion import *
from zlai.types.models_config import *
from zlai.models import app, logger
from zlai.models.config.models import chat_completion_models
from zlai.types.request.completion import ChatCompletionRequest


__all__ = [
    "chat_completions"
]


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """"""
    if len(request.messages) < 1 or request.messages[-1].role == "assistant":
        raise HTTPException(status_code=400, detail="Invalid request, last message role must be user.")

    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        resp_content = f"[ChatCompletion] Models config path: {models_config_path} not exists."
        logger.error(resp_content)
        raise HTTPException(status_code=400, detail=resp_content)
    else:
        logger.info(f"[ChatCompletion] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path).get("models_config")
        model_config = models_config.get(request.model)
        base_config = chat_completion_models.get(request.model)

        if model_config is None or base_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ChatCompletion] Model config: {model_config}")
            base_config.update_kwargs(model_path=model_config.get("model_path"))

        tools_config = ToolsConfig.model_validate(request.model_dump())
        generate_config = base_config.generate_method.model_validate(request.gen_kwargs())
        logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")

        try:
            model_completion = LoadModelCompletion(
                model_config=base_config, model_name=request.model,
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
