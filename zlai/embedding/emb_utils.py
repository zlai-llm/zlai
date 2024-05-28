import json
import requests
from tqdm import tqdm
import numpy as np
from typing import List, Dict, Union, Tuple, Literal, Sequence

from ..schema import *
from ..utils import batches


__all__ = [
    "embedding",
    "embedding_batch",
    "cosine_similarity",
    "top_n_indices",
    "similarity_topn_idx",
    "filter_metrix_by_thresh",
]

headers = {'Content-Type': 'application/json'}


def embedding(
        url: Union[str, EMBUrl],
        text: Union[str, List[str]],
        instruction: bool = False,
        max_len: int = 512,
        max_len_error: Literal['split', 'drop', 'error'] = 'split',
) -> EmbeddingsResponded:
    """
    desc: 计算文本向量
    :param max_len:
    :param max_len_error:
    :param url:
    :param text:
    :param instruction:
    :return:
    """
    if isinstance(text, str):
        text = [text]

    max_text_length = max([len(s) for s in text])

    if max_text_length > max_len:
        if max_len_error == 'split':
            text = [s[:max_len] for s in text]
        elif max_len_error == 'drop':
            text = [s for s in text if len(s) <= max_len]
        elif max_len_error == 'error':
            raise ValueError(f"text max len error, max len is {max_len}, your text len is {max_text_length}.")
        else:
            raise ValueError(f"max_len_error must be 'split', 'drop' or 'error', but got {max_len_error}")

    embedding_request_data = EmbeddingRequest(model='', input=text, instruction=instruction)
    try:
        response = requests.post(url, data=json.dumps(embedding_request_data.model_dump()), headers=headers, timeout=3)
        response.raise_for_status()
        if response.status_code == 200:
            return EmbeddingsResponded.model_validate(response.json())
        else:
            raise requests.exceptions.HTTPError(f"{response.json()}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"RequestException: {e}")


def embedding_batch(
        url,
        data: List[str],
        batch_size: int = 100,
        disp: bool = False,
) -> EmbeddingsResponded:
    """
    desc: 批量计算向量
    :param disp:
    :param url:
    :param data:
    :param batch_size:
    :return:
    """
    total = int(len(data) / batch_size) + 1
    embedding_responds: List[EmbeddingsResponded] = []
    if disp:
        iters = tqdm(batches(data, batch_size=batch_size), total=total)
    else:
        iters = batches(data, batch_size=batch_size)
    for text in iters:
        responded = embedding(url, text=text)
        embedding_responds.append(responded)

    data = sum([respond.data for respond in embedding_responds], [])
    prompt_tokens = sum([respond.usage.prompt_tokens for respond in embedding_responds])
    completion_tokens = sum([respond.usage.completion_tokens for respond in embedding_responds])
    total_tokens = sum([respond.usage.total_tokens for respond in embedding_responds])

    embedding_responded = EmbeddingsResponded(
        object=embedding_responds[0].object,
        data=data,
        model=embedding_responds[0].model,
        usage=CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
    )
    return embedding_responded


def similarity_topn_idx(
        cosine_matrix: np.array,
        axis: int = 1,
        top_n: int = 2,
        ascending: bool = False,
) -> Union[List[List[int]], List[int]]:
    """"""
    if ascending:
        sorted_indices = np.argsort(cosine_matrix, axis=axis)
    else:
        sorted_indices = np.argsort(-cosine_matrix, axis=axis)
    top_n_idx = sorted_indices[:, :top_n].tolist()
    return top_n_idx


def top_n_indices(
        cosine_metrix: np.array,
        axis: int = 1,
        top_n: int = 2,
        **kwargs: Sequence,
) -> Tuple[List[List[float]], Dict[str, Union[str, Sequence]]]:
    """
    desc: 获取相似度最高的top_n个索引
    :param cosine_metrix:
    :param axis:
    :param top_n:
    :param kwargs:
    :return:
    """
    sorted_indices = np.argsort(-cosine_metrix, axis=axis)
    top_n_idx = sorted_indices[:, :top_n].tolist()
    top_n_cosine = [cosine_metrix[i, idx].tolist() for i, idx in enumerate(top_n_idx)]

    top_n_info = {}
    if kwargs:
        for key, val in kwargs.items():
            top_n_info[key] = [np.array(val)[idx].tolist() for idx in top_n_idx]

    return top_n_cosine, top_n_info


def cosine_similarity(
        vector1: np.array,
        vector2: np.array,
) -> np.array:
    """

    :param vector1:
    :param vector2:
    :return:
    """
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1, axis=1, keepdims=True)
    norm_vector2 = np.linalg.norm(vector2, axis=0, keepdims=True)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity


def filter_metrix_by_thresh(
        metrix: Union[List[List[float]], np.array],
        thresh: float = 0.9,
) -> List[List[float]]:
    """"""
    idx = []
    if isinstance(metrix, List):
        metrix = np.array(metrix)

    for row in metrix:
        sorted_id = np.argsort(-row)
        row_id = [idx for idx in sorted_id if row[idx] > thresh]
        idx.append(row_id)
    return idx
