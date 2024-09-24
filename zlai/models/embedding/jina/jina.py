import torch
import torch.nn.functional as F
from typing import Optional, List, Tuple, Any
from zlai.types.response.embedding import *


__all__ = [
    "jina_encode",
]


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


def jina_encode(
        text: List[str],
        model: Any,
        tokenizer: Any,
        batch_size: Optional[int] = 32,
        verbose: Optional[bool] = False,
        normalize_embeddings: Optional[bool] = True,
        device: Optional[str] = None,
        **kwargs,
) -> Tuple[List[List[float]], Usage]:
    """"""
    task = 'retrieval.query'
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors="pt").to(model.device)
    task_id = model._adaptation_map[task]
    adapter_mask = torch.full((len(text),), task_id, dtype=torch.int32).to(model.device)

    with torch.no_grad():
        model_output = model(**encoded_input, adapter_mask=adapter_mask)
    embeddings = mean_pooling(model_output, encoded_input["attention_mask"])
    vectors = F.normalize(embeddings, p=2, dim=1).tolist()
    usage = Usage(total_tokens=sum([len(item) for item in text]))
    return vectors, usage
