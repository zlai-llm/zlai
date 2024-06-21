from .ali import *
from .zhipu import *
from .pretrained import *
from .embedding import *
from .emb_utils import *
from .embedding_config import *
from ..schema import EMBUrl
from typing import Union

TypeEmbedding = Union[Embedding, TypeZhipuEmbedding, TypeAliEmbedding, PretrainedEmbedding]
