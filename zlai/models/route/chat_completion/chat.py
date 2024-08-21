from fastapi import HTTPException
from starlette.responses import StreamingResponse
from zlai.types.models_config import *
from zlai.types.request.completion import ChatCompletionRequest
from ..utils import *
from ...completion import *
from ....models import app, logger


__all__ = [
    "chat_completions"
]


@app.post("/{model_name}/chat/completions")
async def chat_completions(model_name: str, request: ChatCompletionRequest):
    """"""
    model_config = load_model_config(model_name=model_name, inference_name="ChatCompletion")

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
