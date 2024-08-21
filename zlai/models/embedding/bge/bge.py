import torch
from typing import Optional, List, Tuple
from sentence_transformers import SentenceTransformer
from zlai.types.response.embedding import *


__all__ = [
    "encode",
]


def encode(
        text: List[str],
        model: SentenceTransformer,
        batch_size: Optional[int] = 32,
        verbose: Optional[bool] = False,
        normalize_embeddings: Optional[bool] = True,
        device: Optional[str] = None,
        **kwargs,
) -> Tuple[List[List[float]], Usage]:
    """"""
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    usage = Usage(total_tokens=sum([len(item) for item in text]))

    vectors = model.encode(
        sentences=text, batch_size=batch_size, show_progress_bar=verbose,
        device=device, normalize_embeddings=normalize_embeddings,
    ).tolist()
    return vectors, usage
