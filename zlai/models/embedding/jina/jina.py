from typing import Optional, List, Tuple, Any
from zlai.types.response.embedding import *


__all__ = [
    "jina_encode",
]


def jina_encode(
        text: List[str],
        model: Any,
        batch_size: Optional[int] = 32,
        verbose: Optional[bool] = False,
        normalize_embeddings: Optional[bool] = True,
        device: Optional[str] = None,
        **kwargs,
) -> Tuple[List[List[float]], Usage]:
    """"""
    vectors = model.encode(text, task="retrieval.query").tolist()
    usage = Usage(total_tokens=sum([len(item) for item in text]))
    return vectors, usage
