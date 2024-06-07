from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union, Dict
from .base import GenerateConfig
from ...schema import AliModel, Message

__all__ = [
    "TypeAliGenerate",
    # Ali
    "AliGenerateConfig",

    # qwen api
    'AliQwenTurboGenerateConfig',
    'AliQwenPlusGenerateConfig',
    'AliQwenMaxGenerateConfig',
    'AliQwenMax1201GenerateConfig',
    'AliQwenMaxLongContextGenerateConfig',
    # qwen v2
    'AliQwen2Instruct57BA14BGenerateConfig',
    'AliQwen2Instruct72BGenerateConfig',
    'AliQwenInstruct27BGenerateConfig',
    'AliQwen2Instruct15BGenerateConfig',
    'AliQwen2Instruct05BGenerateConfig',
    # qwen v1.5
    'AliQwen15Chat110BGenerateConfig',
    'AliQwen15Chat72BGenerateConfig',
    'AliQwen15Chat32BGenerateConfig',
    'AliQwen15Chat14BGenerateConfig',
    'AliQwen15Chat7BGenerateConfig',
    'AliQwen15Chat18BGenerateConfig',
    'AliQwen15Chat05BGenerateConfig',
    'AliQwen15Code7BGenerateConfig',
    # qwen v1
    'AliQwenChat72BGenerateConfig',
    'AliQwenChat14BGenerateConfig',
    'AliQwenChat7BGenerateConfig',
    'AliQwenChat18BGenerateConfig',
    'AliQwenChat18BLongContextGenerateConfig',
]


class AliVLGenerateConfig(GenerateConfig):
    """"""
    model_config = ConfigDict(protected_namespaces=())
    model_name: AliModel = Field(default=AliModel.qwen_turbo, description="模型名称。", )
    seed: Optional[int] = Field(default=1234, description="生成时使用的随机数种子，用户控制模型生成内容的随机性。", )
    top_p: Optional[float] = Field(default=0.8)
    top_k: Optional[Union[int, None]] = Field(default=100)
    stream: Optional[bool] = Field(default=False)


class AliGenerateConfig(GenerateConfig):
    """"""
    model: Optional[str] = Field(default=..., description="模型名称")
    seed: Optional[int] = Field(default=1234, description="生成时使用的随机数种子，用户控制模型生成内容的随机性。", )
    max_tokens: Optional[int] = Field(default=..., description="""
            用于指定模型在生成内容时token的最大数量，它定义了生成的上限，但不保证每次都会生成到这个数量。
            qwen-turbo最大值和默认值为1500 tokens。
            qwen-max、qwen-max-1201、qwen-max-longcontext和qwen-plus模型，最大值和默认值均为2000 tokens。
            """)
    top_p: Optional[float] = Field(default=0.8, description="""
            生成过程中核采样方法概率阈值。取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高。
            取值为0.8时，仅保留概率加起来大于等于0.8的最可能token的最小集合作为候选集。
            """)
    top_k: Optional[int] = Field(default=None, description="""
            生成时，采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个token组成随机采样的候选集。
            取值越大，生成的随机性越高；取值越小，生成的确定性越高。默认不传递该参数，取值为None或当top_k大于100时，
            表示不启用top_k策略，此时，仅有top_p策略生效。
            """)
    repetition_penalty: Optional[float] = Field(default=1.1, description="""
            用于控制模型生成时的重复度。提高repetition_penalty时可以降低模型生成的重复度。1.0表示不做惩罚。
            """)
    temperature: Optional[float] = Field(default=0.85, description="""
            用于控制随机性和多样性的程度。具体来说，temperature值控制了生成文本时对每个候选词的概率分布进行平滑的程度。
            较高的temperature值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；
            而较低的temperature值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。
            取值范围： [0, 2)，不建议取值为0，无意义。
            """)
    stop: Optional[Union[str, List[str], List[int], List[List[int]]]] = Field(default=None, description="""
            stop参数用于实现内容生成过程的精确控制，在生成内容即将包含指定的字符串或token_ids时自动停止，生成内容不包含指定的内容。
            例如，如果指定stop为"你好"，表示将要生成"你好"时停止；如果指定stop为[37763, 367]，表示将要生成"Observation"时停止。
            stop参数支持以list方式传入字符串数组或者token_ids数组，支持使用多个stop的场景。
            说明: list模式下不支持字符串和token_ids混用，list模式下元素类型要相同。
            """)
    stream: Optional[bool] = Field(default=False, description="""
            是否使用流式输出。当以stream模式输出结果时，接口返回结果为generator，需要通过迭代获取结果，默认每次输出为当前生成的整个序列，
            最后一次输出为最终全部生成结果，可以通过参数incremental_output为False改变输出模式为非增量输出。
            """)
    enable_search: Optional[bool] = Field(default=False, description="""
            模型内置了互联网搜索服务，该参数控制模型在生成文本时是否参考使用互联网搜索结果。取值如下：
            True：启用互联网搜索，模型会将搜索结果作为文本生成过程中的参考信息，但模型会基于其内部逻辑“自行判断”是否使用互联网搜索结果。
            False（默认）：关闭互联网搜索。
            """)
    result_format: Optional[str] = Field(default='message', description="""
            [text|message],默认为text，当为message时，输出参考message结果示例。推荐优先使用message格式。
            """)
    incremental_output: Optional[bool] = Field(default=False, description="""
            控制流式输出模式，即后面内容会包含已经输出的内容；设置为True，将开启增量输出模式，后面输出不会包含已经输出的内容，
            您需要自行拼接整体输出，参考流式输出示例代码。
            """)
    tools: Optional[List[str]] = Field(default=None, description="""
            模型可选调用的工具列表。目前仅支持function，并且即使输入多个function，模型仅会选择其中一个生成结果。
            模型根据tools参数内容可以生产函数调用的参数。
            """)
    messages: Union[List[Dict], List[Message]] = Field(default=[])


class AliQwen2Instruct57BA14BGenerateConfig(AliGenerateConfig):
    """ qwen2-57b-a14b-instruct
    通义千问2对外开源的57B规模14B激活参数的MOE模型
    模型支持 32,768 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为 30,720 ，输出最大 6,144。
    """
    model: Optional[str] = Field(default="qwen2-57b-a14b-instruct", description="模型名称")
    max_tokens: Optional[int] = Field(default=6144, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen2Instruct72BGenerateConfig(AliGenerateConfig):
    """qwen2-72b-instruct
    通义千问2对外开源的0.5~72B规模的模型
    模型支持 131,072 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为 128,000 ，输出最大 6,144。
    """
    model: Optional[str] = Field(default="qwen2-72b-instruct", description="模型名称")
    max_tokens: Optional[int] = Field(default=6144, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenInstruct27BGenerateConfig(AliGenerateConfig):
    """qwen2-7b-instruct
    通义千问2对外开源的0.5~72B规模的模型
    模型支持 131,072 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为 128,000 ，输出最大 6,144。
    """
    model: Optional[str] = Field(default="qwen2-7b-instruct", description="模型名称")
    max_tokens: Optional[int] = Field(default=6144, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen2Instruct15BGenerateConfig(AliGenerateConfig):
    """qwen2-1.5b-instruct
    通义千问2对外开源的0.5~72B规模的模型
    模型支持 131,072 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为 128,000 ，输出最大 6,144。
    """
    model: Optional[str] = Field(default="qwen2-1.5b-instruct", description="模型名称")
    max_tokens: Optional[int] = Field(default=6144, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen2Instruct05BGenerateConfig(AliGenerateConfig):
    """qwen2-0.5b-instruct
    通义千问2对外开源的0.5~72B规模的模型
    模型支持 131,072 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为 128,000 ，输出最大 6,144。
    """
    model: Optional[str] = Field(default="qwen2-0.5b-instruct", description="模型名称")
    max_tokens: Optional[int] = Field(default=6144,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenTurboGenerateConfig(AliGenerateConfig):
    """ qwen-turbo
    通义千问超大规模语言模型，支持中文、英文等不同语言输入。
    模型支持8k tokens上下文，为了保证正常的使用和输出，API限定用户输入为6k tokens。
    """
    model: Optional[str] = Field(default="qwen-turbo", description="模型名称")
    max_tokens: Optional[int] = Field(default=1500, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenPlusGenerateConfig(AliGenerateConfig):
    """ qwen-plus
    通义千问超大规模语言模型增强版，支持中文、英文等不同语言输入。
    模型支持32k tokens上下文，为了保证正常的使用和输出，API限定用户输入为30k tokens。
    """
    model: Optional[str] = Field(default="qwen-plus", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenMaxGenerateConfig(AliGenerateConfig):
    """ qwen-max
    通义千问千亿级别超大规模语言模型，支持中文、英文等不同语言输入。随着模型的升级，qwen-max将滚动更新升级，如果希望使用稳定版本，请使用qwen-max-1201。
    模型支持8k tokens上下文，为了保证正常的使用和输出，API限定用户输入为6k tokens。
    """
    model: Optional[str] = Field(default="qwen-max", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenMax1201GenerateConfig(AliGenerateConfig):
    """ qwen-max-1201
    通义千问千亿级别超大规模语言模型，支持中文、英文等不同语言输入。该模型为qwen-max的快照稳定版本，预期维护到下个快照版本发布时间（待定）后一个月。
    模型支持8k tokens上下文，为了保证正常的使用和输出，API限定用户输入为6k tokens。
    """
    model: Optional[str] = Field(default="qwen-max-1201", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenMaxLongContextGenerateConfig(AliGenerateConfig):
    """ qwen-max-longcontext
    通义千问千亿级别超大规模语言模型，支持中文、英文等不同语言输入。
    模型支持30k tokens上下文，为了保证正常的使用和输出，API限定用户输入为28k tokens。
    """
    model: Optional[str] = Field(default="qwen-max-longcontext", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat110BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-110b-chat
    通义千问1.5对外开源的110B规模参数量的经过人类指令对齐的chat模型
    模型支持 32,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为30,000，输出最大 8,000。
    """
    model: Optional[str] = Field(default="qwen1.5-110b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=8000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat72BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-72b-chat
    通义千问1.5对外开源的72B规模参数量的经过人类指令对齐的chat模型
    支持32k tokens上下文，输入最大30k，输出最大2k tokens。
    """
    model: Optional[str] = Field(default="qwen1.5-72b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat32BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-32b-chat
    通义千问1.5对外开源的32B规模参数量的经过人类指令对齐的chat模型
    支持32k tokens上下文，输入最大30k，输出最大2k tokens。
    """
    model: Optional[str] = Field(default="qwen1.5-32b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat14BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-14b-chat
    通义千问1.5对外开源的14B规模参数量的经过人类指令对齐的chat模型
    模型支持 8,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为6,000，输出最大 2,000。
    """
    model: Optional[str] = Field(default="qwen1.5-14b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat7BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-7b-chat
    通义千问1.5对外开源的7B规模参数量的经过人类指令对齐的chat模型
    模型支持 8,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为6,000，输出最大 2,000。
    """
    model: Optional[str] = Field(default="qwen1.5-7b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat18BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-1.8b-chat
    通义千问1.5对外开源的1.8B规模参数量的经过人类指令对齐的chat模型
    模型支持 32,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为30,000，输出最大 2,000。
    """
    model: Optional[str] = Field(default="qwen1.5-1.8b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Chat05BGenerateConfig(AliGenerateConfig):
    """ qwen1.5-0.5b-chat
    通义千问1.5对外开源的1.8B规模参数量的经过人类指令对齐的chat模型
    模型支持 32,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为30,000，输出最大 2,000。
    """
    model: Optional[str] = Field(default="qwen1.5-0.5b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwen15Code7BGenerateConfig(AliGenerateConfig):
    """ codeqwen1.5-7b-chat
    通义千问1.5对外开源的7B规模参数量的经过人类指令对齐的针对代码场景的chat模型
    模型支持 64,000 tokens上下文，为了保障正常使用和正常输出，API限定用户输入为56,000，输出最大 8,000。
    """
    model: Optional[str] = Field(default="codeqwen1.5-7b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=8000, description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenChat72BGenerateConfig(AliGenerateConfig):
    """ qwen-72b-chat
    通义千问对外开源的72B规模参数量的经过人类指令对齐的chat模型
    支持32k tokens上下文，输入最大30k，输出最大2k tokens。
    """
    model: Optional[str] = Field(default="qwen-72b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenChat14BGenerateConfig(AliGenerateConfig):
    """ qwen-14b-chat
    通义千问对外开源的14B规模参数量的经过人类指令对齐的chat模型
    模型支持 8k tokens上下文，为了保障正常使用和正常输出，API限定用户输入为6k Tokens。
    """
    model: Optional[str] = Field(default="qwen-14b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenChat7BGenerateConfig(AliGenerateConfig):
    """ qwen-7b-chat
    通义千问对外开源的7B规模参数量的经过人类指令对齐的chat模型
    """
    model: Optional[str] = Field(default="qwen-7b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenChat18BGenerateConfig(AliGenerateConfig):
    """ qwen-1.8b-chat
    通义千问对外开源的1.8B规模参数量的经过人类指令对齐的chat模型
    模型支持 8k tokens上下文，为了保障正常使用和正常输出，API限定用户输入为6k Tokens。
    """
    model: Optional[str] = Field(default="qwen-1.8b-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


class AliQwenChat18BLongContextGenerateConfig(AliGenerateConfig):
    """ qwen-1.8b-longcontext-chat
    通义千问对外开源的1.8B规模参数量的经过人类指令对齐的chat模型
    支持32k tokens上下文，输入最大30k，输出最大2k tokens。
    """
    model: Optional[str] = Field(default="qwen-1.8b-longcontext-chat", description="模型名称")
    max_tokens: Optional[int] = Field(default=2000,
                                      description="""用于指定模型在生成内容时token的最大数量，它定义了生成的上限。""")


TypeAliGenerate = Union[
    AliGenerateConfig,
    # qwen api
    AliQwenTurboGenerateConfig,
    AliQwenPlusGenerateConfig,
    AliQwenMaxGenerateConfig,
    AliQwenMax1201GenerateConfig,
    AliQwenMaxLongContextGenerateConfig,
    # qwen v2
    AliQwen2Instruct57BA14BGenerateConfig,
    AliQwen2Instruct72BGenerateConfig,
    AliQwenInstruct27BGenerateConfig,
    AliQwen2Instruct15BGenerateConfig,
    AliQwen2Instruct05BGenerateConfig,
    # qwen v1.5
    AliQwen15Chat110BGenerateConfig,
    AliQwen15Chat72BGenerateConfig,
    AliQwen15Chat32BGenerateConfig,
    AliQwen15Chat14BGenerateConfig,
    AliQwen15Chat7BGenerateConfig,
    AliQwen15Chat18BGenerateConfig,
    AliQwen15Chat05BGenerateConfig,
    AliQwen15Code7BGenerateConfig,
    # qwen v1
    AliQwenChat72BGenerateConfig,
    AliQwenChat14BGenerateConfig,
    AliQwenChat7BGenerateConfig,
    AliQwenChat18BGenerateConfig,
    AliQwenChat18BLongContextGenerateConfig,
]
