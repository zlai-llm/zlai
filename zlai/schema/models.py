from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel

__all__ = [
    "Remote",
    # Remote LLM model
    "ModelName",
    "AliModel",
    "ZhipuModel",

    # Remote EMB model
    "EmbeddingsModel",
    "ZhipuEmbeddingModel",
]


class Remote(str, Enum):
    """ 远程服务列表 """
    zhipu: str = 'zhipu'  # https://open.bigmodel.cn/
    ali: str = 'ali'      # https://help.aliyun.com/zh/dashscope
    # baidu = 'baidu'  # TODO


class ModelName(str, Enum):
    """ 模型名称 """


class AliModel(ModelName):
    """"""
    bailian_v1 = 'bailian-v1'
    dolly_12b_v2 = 'dolly-12b-v2'
    qwen_turbo = 'qwen-turbo'
    qwen_plus = 'qwen-plus'
    qwen_max = 'qwen-max'
    qwen_vl_plus = "qwen-vl-plus"


class ZhipuModel(ModelName):
    """"""
    # V1 后续弃用
    chatglm_turbo = 'chatglm_turbo'
    # V2 GLM-4
    glm_4 = 'glm-4'
    glm_3_turbo = 'glm-3-turbo'
    emb2 = "embedding-2"


class EmbeddingsModel(str, Enum):
    """"""


@dataclass
class ZhipuEmbeddingModel(EmbeddingsModel):
    """"""
    emb2 = "embedding-2"
