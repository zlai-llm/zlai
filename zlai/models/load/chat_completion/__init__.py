from .mini_cpm import *
from .glm4 import *
from .qwen2 import *
from .codegeex import *
from .deepseek import *


load_method_mapping = {
    "load_qwen2_audio": load_qwen2_audio,
    "load_qwen2": load_qwen2,
    "load_glm4": load_glm4,
    "load_mini_cpm": load_mini_cpm,
}
