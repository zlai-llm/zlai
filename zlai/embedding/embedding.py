import os
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from functools import lru_cache
from typing import Any, List, Union, Tuple, Callable, Literal, Optional

from ..utils import *
from ..schema import *
from .emb_utils import *


__all__ = [
    "Embedding",
    "EmbeddingMixin",
    "EmbeddingCompletion",
]

headers = {'Content-Type': 'application/json'}

emb_url = EMBUrl()


class EmbeddingCompletion(LoggerMixin):
    """"""
    emb_url: Union[str, EMBUrl, None] = emb_url.bge_m3
    model_name: Optional[EmbeddingsModel] = None
    max_len: int = 512
    instruction: bool = False
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    model_path = Optional[str]
    batch_size = Optional[int]
    api_key: Optional[str] = None
    api_key_name: Optional[str] = None
    verbose: bool = False
    logger: Optional[Callable] = None

    @classmethod
    def trans_input_text(cls, text: Union[str, List[str]],) -> List[str]:
        """"""
        if isinstance(text, str):
            text = [text]
        return text

    @classmethod
    def trans_vectors(cls, vectors: List[List[float]]) -> List[Vector]:
        """"""
        return [Vector(object='vector', index=i, embedding=vec) for i, vec in enumerate(vectors)]

    @classmethod
    def trans_obj_vectors(cls, vectors: List[Vector]) -> List[List[float]]:
        """"""
        return [vec.embedding for vec in vectors]

    @classmethod
    def trans_numpy(cls, vectors: List[Vector]) -> np.ndarray:
        """"""
        return np.array(cls.trans_obj_vectors(vectors))

    @classmethod
    def tokens_usage(cls, text: List[str]) -> CompletionUsage:
        """"""
        tokens = sum([len(sample) for sample in text])
        usage = CompletionUsage(
            completion_tokens=tokens,
            prompt_tokens=0,
            total_tokens=tokens,
        )
        return usage

    def batch_iter(self, items: List[Any]):
        """"""
        if self.verbose:
            iters = tqdm(batches(items, batch_size=self.batch_size), total=int(len(items) / self.batch_size) + 1)
        else:
            iters = batches(items, batch_size=self.batch_size)
        return iters

    @lru_cache()
    def from_pretrained(self):
        """"""
        from sentence_transformers import SentenceTransformer
        if self.model_path:
            self._logger(msg="Loading model ...", color="green")
            model = SentenceTransformer(self.model_path)
            self._logger(msg="Success load model ...", color="green")
            return model
        else:
            raise ValueError(f"Path: {self.model_path} not find.")

    def pretrained_model_embedding(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        """"""
        text = self.trans_input_text(text=text)
        usage = self.tokens_usage(text=text)
        model = self.from_pretrained()

        vectors = []
        iters = self.batch_iter(items=text)
        for one_batch in iters:
            one_batch_vectors = model.encode(one_batch)
            vectors.extend(one_batch_vectors)

        data = self.trans_vectors(vectors=vectors)
        emb_output = EmbeddingsResponded(object='list', data=data, model=self.model_path, usage=usage)
        return emb_output

    def local_embedding(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        """"""
        text = self.trans_input_text(text=text)
        usage = self.tokens_usage(text=text)

        if self.emb_url is not None:
            # model_name = self.emb_metadata.get(self.emb_url)
            emb_output = embedding_batch(url=self.emb_url, data=text, batch_size=self.batch_size, disp=self.verbose)
            return emb_output
        else:
            raise ValueError(f"{self.emb_url} is not supported.")

    @lru_cache(maxsize=128)
    def embedding(
            self,
            text: Union[str, List[str], Tuple[str, ...]],
    ) -> EmbeddingsResponded:
        """"""
        text = self.trans_input_text(text=text)
        if self.emb_url:
            return self.local_embedding(text=text)
        elif self.model_path:
            return self.pretrained_model_embedding(text=text)
        else:
            raise ValueError(f"{self.emb_url} or {self.model_name} is not supported.")


class EmbeddingMixin(EmbeddingCompletion):
    """"""
    emb_url: Union[str, EMBUrl, None] = emb_url.bge_m3
    model_name: Optional[EmbeddingsModel] = None
    max_len: int = 512
    instruction: bool = False
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    verbose: bool = False

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)

    def trans_any_vectors(self, vectors: Union[EmbeddingsResponded, np.ndarray, List[List[float]]]) -> np.ndarray:
        """"""
        if isinstance(vectors, EmbeddingsResponded):
            return vectors.to_numpy()
        elif isinstance(vectors, List):
            return np.array(vectors)
        elif isinstance(vectors, np.ndarray):
            return vectors
        else:
            raise TypeError(f"vectors type must in [EmbeddingsResponded, np.ndarray, List[List[float]].")

    def _similarity_matrix(
            self,
            source: Optional[List[str]] = None,
            target: Optional[List[str]] = None,
            source_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
            target_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
    ) -> np.ndarray:
        """"""
        if source_vector is not None and target_vector is not None:
            source_vector = self.trans_any_vectors(vectors=source_vector)
            target_vector = self.trans_any_vectors(vectors=target_vector)
        elif source is not None and target is not None:
            source_vector = self.embedding(tuple(source)).to_numpy()
            target_vector = self.embedding(tuple(target)).to_numpy()
        else:
            raise ValueError(f"should give source-target pair or source_vector-target_vector pair.")
        matrix = cosine_similarity(source_vector, target_vector.T)
        return matrix

    def _match(self,
               source: Optional[List[str]] = None,
               target: Optional[List[str]] = None,
               source_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
               target_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
               top_n: Optional[int] = 1,
               thresh: Optional[float] = None,
               filter: Optional[Literal['top_n', 'thresh', 'union']] = None
    ) -> Tuple[List[List[int]], np.ndarray]:
        """"""
        if len(source) == 0 or len(target) == 0:
            raise ValueError(f"Empty source or target list. Source: {source}, Target: {target}.")

        matrix = self._similarity_matrix(source=source, target=target, source_vector=source_vector, target_vector=target_vector)
        self._logger(f"[Embedding] params: top_n: {top_n}, thresh: {thresh}, filter: {filter}", color="green")
        if filter == 'top_n':
            if top_n is None:
                raise ValueError(f"need to set param top_n.")
            idx = similarity_topn_idx(cosine_matrix=matrix, axis=1, top_n=top_n, ascending=False)
        elif filter == 'thresh':
            if thresh is None:
                raise ValueError(f"need to set param thresh.")
            idx = filter_metrix_by_thresh(metrix=matrix, thresh=thresh)
        elif filter == 'union':
            if top_n is None or thresh is None:
                raise ValueError(f"need to set param thresh and top n.")
            idx = filter_metrix_by_thresh(metrix=matrix, thresh=thresh)
            idx = [_id[:top_n] for _id in idx]
        else:
            raise ValueError(f"{filter} is not supported.")
        return idx, matrix

    def _match_keyword(
            self,
            source: List[str],
            target: List[str],
            thresh: Optional[float] = 0.7,
            keyword_method: Literal["content", "keyword"] = "keyword",
    ) -> List[EmbeddingMatchOutput]:
        """"""
        keyword_match = []
        src_dst_keywords_mapping = defaultdict(list)
        if keyword_method == "content":
            target_content = '/'.join(target)
            for src in source:
                if src in target_content:
                    src_dst_keywords_mapping[src] = target
        elif keyword_method == 'keyword':
            for src in source:
                for tar in target:
                    if src in tar:
                        src_dst_keywords_mapping[src].append(tar)
        else:
            raise ValueError(f"{keyword_method} is not supported.")

        for src_keyword, tar_lst in src_dst_keywords_mapping.items():
            keyword_score = self._similarity_matrix(source=[src_keyword], target=tar_lst)[0]
            if keyword_score.max() > thresh:
                idx = keyword_score.argsort()[-1]
                keyword_match.append(EmbeddingMatchOutput(
                    src=src_keyword,
                    dst=[tar_lst[idx]],
                    score=[keyword_score[idx]],
                    match_type=["keyword"],
                    keyword_method=keyword_method,
                ))
        return keyword_match

    @classmethod
    def _merge_match_output(
            cls,
            *args: List[EmbeddingMatchOutput],
    ) -> List[EmbeddingMatchOutput]:
        """"""
        exit_src_name = []
        drop_duplicate_match = []
        match_output = sum(args, [])
        for output in match_output:
            if output.src not in exit_src_name:
                exit_src_name.append(output.src)
                drop_duplicate_match.append(output)
            else:
                exit_idx = exit_src_name.index(output.src)
                for i, dst_item in enumerate(output.dst):
                    if dst_item not in drop_duplicate_match[exit_idx].dst:
                        drop_duplicate_match[exit_idx].dst.append(dst_item)
                        drop_duplicate_match[exit_idx].score.append(output.score[i])
                drop_duplicate_match[exit_idx].match_type.extend(output.match_type)
        return drop_duplicate_match

    def match(
            self,
            source: Optional[List[str]] = None,
            target: Optional[List[str]] = None,
            source_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
            target_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
            top_n: Optional[int] = 1,
            thresh: Optional[float] = None,
            filter: Optional[Literal['top_n', 'thresh', 'union']] = None
    ) -> List[EmbeddingMatchOutput]:
        idx, metrix = self._match(
            source=source, target=target, source_vector=source_vector, target_vector=target_vector,
            top_n=top_n, thresh=thresh, filter=filter)
        match_output = []
        for src, _ids, _score in zip(source, idx, metrix):
            dst = [target[_id] for _id in _ids]
            score = [_score[_id] for _id in _ids]
            if len(_ids) > 0:
                embedding_match_output = EmbeddingMatchOutput(src=src, dst=dst, score=score, target=dst)
                match_output.append(embedding_match_output)
            else:
                embedding_match_output = EmbeddingMatchOutput(src=src, dst=[], score=score, target=dst)
                match_output.append(embedding_match_output)
        return match_output

    def match_idx(
            self,
            source: Optional[List[str]] = None,
            target: Optional[List[str]] = None,
            source_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
            target_vector: Optional[Union[EmbeddingsResponded, np.ndarray, List[List[float]]]] = None,
            top_n: Optional[int] = 1,
            thresh: Optional[float] = None,
            filter: Literal['top_n', 'thresh', 'union'] = 'top_n'
    ) -> List[List[int]]:
        """

        :param source:
        :param target:
        :param source_vector:
        :param target_vector:
        :param top_n:
        :param thresh:
        :param filter:
        :return:
        """

        idx, _ = self._match(
            source=source, target=target, source_vector=source_vector, target_vector=target_vector,
            top_n=top_n, thresh=thresh, filter=filter)
        return idx

    def match_with_keyword(
            self,
            source: List[str],
            target: List[str],
            top_n: Optional[int] = None,
            thresh: Optional[Tuple[float, float]] = (0.9, 0.7),
            filter: Literal['top_n', 'thresh', 'union'] = 'thresh',
            keyword_method: Literal["content", "keyword"] = "keyword",
            drop_duplicate: bool = True,
    ) -> List[EmbeddingMatchOutput]:
        """"""
        upper_thresh, lower_thresh = thresh
        score_match = self.match(source=source, target=target, top_n=top_n, thresh=upper_thresh, filter=filter)
        keyword_match = self._match_keyword(
            source=source, target=target, thresh=lower_thresh, keyword_method=keyword_method)
        if drop_duplicate:
            return self._merge_match_output(score_match, keyword_match)
        else:
            return score_match + keyword_match


class Embedding(EmbeddingMixin):
    """"""
    emb_url: Union[str, EMBUrl, None] = emb_url.bge_m3
    model_name: Optional[EmbeddingsModel] = None
    max_len: int = 512
    instruction: bool = False
    max_len_error: Literal['split', 'drop', 'error'] = 'split'
    verbose: bool = False
    model_path = Optional[str]
    batch_size = Optional[int]
    logger: Optional[Callable]
    verbose: Optional[bool]

    def __init__(
            self,
            emb_url: Union[str, EMBUrl, None] = None,
            model_name: Optional[EmbeddingsModel] = None,
            model_path: Optional[str] = None,
            batch_size: int = 128,
            max_len: int = 512,
            instruction: bool = False,
            max_len_error: Literal['split', 'drop', 'error'] = 'split',
            verbose: bool = False,
            logger: Optional[Callable] = None,
            **kwargs
    ):
        """"""
        self.verbose = verbose
        self.logger = logger

        # local
        self.emb_url = emb_url
        self.model_name = model_name
        self.max_len = max_len
        self.instruction = instruction
        self.max_len_error = max_len_error
        # self.emb_metadata = get_dataclass_metadata(cls=EMBUrl)

        # from pretrained model
        self.model_path = model_path
        self.batch_size = batch_size

    def __call__(
            self,
            text: Union[str, List[str]],
    ) -> EmbeddingsResponded:
        if isinstance(text, str):
            text = [text]
        return self.embedding(text=text)
