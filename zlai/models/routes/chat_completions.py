import os
import time
from fastapi import HTTPException
from starlette.responses import StreamingResponse
from typing import List, Dict, Union
from zlai.types import *
from zlai.models.types.schema import *
from zlai.utils.config import pkg_config
from ..completion import *
from ..utils import load_model_config
from ...models import app, logger
from ..completion.glm4.utils import ParseFunctionCall


__all__ = [
    "chat_completions"
]


def get_model_config(
        model_name: str,
        models_config: List[Dict],
) -> Union[Dict, None]:
    """"""
    for config in models_config:
        if config["model_name"] == model_name:
            return config
    return None


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """"""
    if len(request.messages) < 1 or request.messages[-1].role == "assistant":
        raise HTTPException(status_code=400, detail="Invalid request, last message role must be user.")

    models_config_path = os.path.join(pkg_config.cache_path, "models_config.yml")
    if not os.path.exists(models_config_path):
        logger.error(f"[ChatCompletion] Models config path: {models_config_path} not exists.")
        resp_content = "Error: Models config path not exists."
    else:
        logger.info(f"[ChatCompletion] Models config path: {models_config_path}")
        models_config = load_model_config(path=models_config_path)
        models_config = models_config.get("models_config")
        model_config = get_model_config(model_name=request.model, models_config=models_config)

        if model_config is None:
            raise HTTPException(status_code=400, detail="Invalid request, model not exists.")
        else:
            logger.info(f"[ChatCompletion] Model config: {model_config}")
            model_config = ModelConfig.model_validate(model_config)

        tools_config = ToolsConfig.model_validate(request.model_dump())
        generate_config = model_config.generate_method.model_validate(request.model_dump())
        logger.info(f"[ChatCompletion] Generate kwargs: {generate_config.gen_kwargs()}")

        model_completion = LoadModelCompletion(
            models_config=models_config, model_name=request.model,
            generate_config=generate_config, tools_config=tools_config,
            logger=logger)

        if request.stream:
            return StreamingResponse(
                model_completion.stream_completion(messages=request.messages),
                media_type="application/x-ndjson")
        else:
            resp_content = model_completion.completion(messages=request.messages)

    if request.tools:
        parse_function_call = ParseFunctionCall(content=resp_content, tools=request.tools)
        chat_completion_message = parse_function_call.to_chat_completion_message()
        if chat_completion_message.content is None and chat_completion_message.tool_calls:
            finish_reason = "tool_calls"
        else:
            finish_reason = "stop"
    else:
        chat_completion_message = ChatCompletionMessage(role="assistant", content=resp_content)
        finish_reason = "stop"

    choice = Choice(finish_reason=finish_reason, index=0, message=chat_completion_message)
    chat_completion = ChatCompletion(
        id="1337",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[choice]
    )
    return chat_completion
