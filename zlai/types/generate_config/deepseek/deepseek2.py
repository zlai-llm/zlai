from typing import Union
from zlai.types.generate_config.base import GenerateConfig


__all__ = [
    "DeepSeekGenerateConfig",
    "TypeDeepSeekGenerate",
    "DeepSeekV2LiteChatGenerateConfig",
    "DeepSeekCoderV2LiteInstructChatGenerateConfig",
]


class DeepSeekGenerateConfig(GenerateConfig):
    """"""
    temperature: float = 0.3
    top_p: float = 0.95


class DeepSeekV2LiteChatGenerateConfig(DeepSeekGenerateConfig):
    """"""
    do_sample: bool = True
    max_new_tokens: int = 1024


class DeepSeekCoderV2LiteInstructChatGenerateConfig(DeepSeekGenerateConfig):
    """"""
    top_k: int = 50
    do_sample: bool = False
    max_new_tokens: int = 512
    num_return_sequences: int = 1


TypeDeepSeekGenerate = Union[
    DeepSeekGenerateConfig,
    DeepSeekV2LiteChatGenerateConfig,
    DeepSeekCoderV2LiteInstructChatGenerateConfig,
]
