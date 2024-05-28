from enum import Enum
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from typing import Union

__all__ = [
    "LLMUrl",
    "BaseUrl",
    "ESUrl",
    "EMBUrl",
    "Model",
    "EmbeddingModel",
]


class BaseUrl(BaseModel):
    """"""
    def change_url_port(self, origin_port, new_port):
        """"""
        for field, value in self.model_dump().items():
            if isinstance(value, str) and value.startswith('http://'):
                setattr(self, field, value.replace(f':{origin_port}', f':{new_port}'))

    def apply_address(self, host: str, port: Union[int, str]):
        """"""
        for field, value in self.model_dump().items():
            if "port" in value:
                setattr(self, field, value.replace('port', port))
            if "host" in value:
                setattr(self, field, value.replace('host', host))


class LLMUrl(BaseUrl):
    # chatglm
    chatglm3_6b: str = 'host:port/llm/chatglm3_6b'
    chatglm3_6b_32k: str = 'host:port/llm/chatglm3_6b_32k'
    chatglm3_6b_128k: str = 'host:port/llm/chatglm3_6b_128k'
    chatglm3_6b_base: str = 'host:port/llm/chatglm3_6b_base'

    # baichuan2
    baichuan2_7b_chat: str = 'host:port/llm/baichuan2_7b_chat'
    baichuan2_13b_chat: str = 'host:port/llm/baichuan2_13b_chat'

    # qwen
    qwen_1_8b_chat: str = 'host:port/llm/qwen_1_8b_chat'
    qwen_7b_chat: str = 'host:port/llm/qwen_7b_chat'
    qwen_14b_chat: str = 'host:port/llm/qwen_14b_chat'
    qwen_1_5_7b_chat: str = 'host:port/llm/qwen1.5_7b_chat'
    qwen_1_5_14b_chat: str = 'host:port/llm/qwen1.5_14b_chat'
    qwen_1_5_72b_chat_awq: str = 'host:port/llm/qwen1.5_72b_chat_awq'
    qwen_1_5_72b_chat_init4: str = 'host:port/llm/qwen1.5_72b_chat_gptq_int4'
    qwen_1_5_72b_chat_init8: str = 'host:port/llm/qwen1.5_72b_chat_gptq_int8'
    qwen_vl_chat: str = 'host:port/llm/qwen_vl_chat'

    # llama
    llama_coder_7b_instruct: str = 'host:port/llm/llama_coder_7b_instruct'
    llama_coder_33b_instruct: str = 'host:port/llm/llama_coder_33b_instruct'

    # internlm
    # internlm_chat_7b: str = "host:port/llm/internlm_chat_7b"
    # internlm_chat_20b: str = "host:port/llm/internlm_chat_20b"

    # yi
    # yi_34b_chat: str = "host:port/llm/yi_34b_chat"
    # yi_34b_200k: str = "host:port/llm/yi_34b_200k"
    # yi_6b_chat: str = "host:port/llm/yi_6b_chat"
    # yi_6b_200k: str = "host:port/llm/yi_6b_200k"


class EMBUrl(BaseUrl):
    # BGE
    bge_large: str = 'host:port/embedding/bge_large'
    bge_base: str = 'host:port/embedding/bge_base'
    bge_small: str = 'host:port/embedding/bge_small'
    bge_m3: str = 'host:port/embedding/bge_m3'
    # M3E
    m3e_large: str = 'host:port/embedding/m3e_large'
    m3e_base: str = 'host:port/embedding/m3e_base'
    m3e_small: str = 'host:port/embedding/m3e_small'


class ESUrl(BaseUrl):
    """"""
    url: str = "http://host:port/"


class GPUCache(BaseUrl):
    """"""
    delete: str = 'host:port/cache/delete'
    gpu_info: str = 'host:port/cache/gpu_info'
    check: str = 'host:port/cache/check'


class Model(LLMUrl):
    """"""


class EmbeddingModel(EMBUrl):
    """"""
