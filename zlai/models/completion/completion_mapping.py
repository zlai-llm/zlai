from .qwen2 import *
from .glm4 import *
from .mini_cpm import *
from .deepseek import *
from .codegeex import *


__all__ = [
    "completion_mapping",
    "stream_completion_mapping",
]

qwen2_models = [
    "Qwen2-Audio-7B-Instruct",
    "Qwen2-0.5B-Instruct",
    "Qwen2-1.5B-Instruct",
    "Qwen2-7B-Instruct",
    "Qwen2-57B-A14B-Instruct-GPTQ-Int4",
]
qwen2_completion_mapping = dict.fromkeys(qwen2_models, completion_qwen_2)
qwen2_stream_completion_mapping = dict.fromkeys(qwen2_models, stream_completion_qwen_2)


glm_4_models = [
    "glm-4-9b-chat",
    "glm-4-9b-chat-1m",
    "glm-4v-9b",
]
glm_4_completion_mapping = dict.fromkeys(glm_4_models, completion_glm_4)
glm_4_stream_completion_mapping = dict.fromkeys(glm_4_models, stream_completion_glm_4)


mini_cpm_models = [
    "mini_cpm-v2_6",
]
mini_cpm_completion_mapping = dict.fromkeys(mini_cpm_models, completion_mini_cpm)
mini_cpm_stream_completion_mapping = dict.fromkeys(mini_cpm_models, stream_completion_mini_cpm)


deepseek_v2_models = [
    "DeepSeek-V2-Lite-Chat"
]
deepseek_completion_mapping = dict.fromkeys(deepseek_v2_models, completion_deepseek_2)
deepseek_stream_completion_mapping = dict.fromkeys(deepseek_v2_models, stream_completion_deepseek_2)


deepseek_coder_v2_models = [
    "DeepSeek-Coder-V2-Lite-Instruct"
]
deepseek_coder_v2_completion_mapping = dict.fromkeys(deepseek_coder_v2_models, completion_deepseek_coder_v2)
deepseek_coder_v2_stream_completion_mapping = dict.fromkeys(deepseek_coder_v2_models, stream_completion_deepseek_coder_v2)


codegeex_4_models = [
    "codegeex4-all-9b"
]
codegeex_4_completion_mapping = dict.fromkeys(codegeex_4_models, completion_codegeex_4)
codegeex_4_stream_completion_mapping = dict.fromkeys(codegeex_4_models, stream_completion_codegeex_4)


completion_mapping = {
    **qwen2_completion_mapping,
    **glm_4_completion_mapping,
    **mini_cpm_completion_mapping,
    **codegeex_4_completion_mapping,
}

stream_completion_mapping = {
    **qwen2_stream_completion_mapping,
    **glm_4_stream_completion_mapping,
    **mini_cpm_stream_completion_mapping,
    **codegeex_4_stream_completion_mapping,
}
