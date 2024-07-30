from typing import Literal, Optional
from pydantic import BaseModel, Field


__all__ = [
    "Model",
    "ModelList",
    "_model_list",
]


class Model(BaseModel):
    id: str = Field(description="""The model identifier, which can be referenced in the API endpoints.""")
    created: Optional[int] = Field(default=None, description="""The Unix timestamp (in seconds) when the model was created.""")
    object: Literal["model"] = Field(default="model", description="""The object type, which is always "model".""")
    owned_by: Optional[str] = Field(default="Open Source", description="""The organization that owns the model.""")


class ModelList(BaseModel):
    """"""
    qwen_2_05b_instruct: str = "Qwen2-0.5B-Instruct"
    qwen_2_15b_instruct: str = "Qwen2-1.5B-Instruct"
    qwen_2_7b_instruct: str = "Qwen2-7B-Instruct"
    qwen_2_57b_a14b_instruct_gptq_int4: str = "Qwen2-57B-A14B-Instruct-GPTQ-Int4"
    glm_4_9b_chat: str = "glm-4-9b-chat"
    glm_4_9b_chat_1m: str = "glm-4-9b-chat-1m"
    glm_4_9b: str = "glm-4v-9b"


_model_list = ModelList()

