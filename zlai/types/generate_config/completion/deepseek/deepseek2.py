from typing import Union, Optional
from zlai.types.generate_config.completion.base import GenerateConfig


__all__ = [
    "DeepSeekGenerateConfig",
    "TypeDeepSeekGenerate",
    "DeepSeekV2LiteChatGenerateConfig",
    "DeepSeekCoderV2LiteInstructChatGenerateConfig",
]


class DeepSeekGenerateConfig(GenerateConfig):
    """"""
    temperature: Optional[float] = 0.3
    top_p: Optional[float] = 0.95


class DeepSeekV2LiteChatGenerateConfig(DeepSeekGenerateConfig):
    """"""
    do_sample: Optional[bool] = True
    max_new_tokens: Optional[int] = 1024


class DeepSeekCoderV2LiteInstructChatGenerateConfig(DeepSeekGenerateConfig):
    """"""
    top_k: Optional[int] = 50
    do_sample: Optional[bool] = False
    max_new_tokens: Optional[int] = 512
    num_return_sequences: Optional[int] = 1


TypeDeepSeekGenerate = Union[
    DeepSeekGenerateConfig,
    DeepSeekV2LiteChatGenerateConfig,
    DeepSeekCoderV2LiteInstructChatGenerateConfig,
]
