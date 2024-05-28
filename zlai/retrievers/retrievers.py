import re
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Literal, Callable
from ..embedding import cosine_similarity, similarity_topn_idx

np.random.seed(0)

__all__ = [
    "TextPrepareBase",
    "PolicySupportText",
]


# todo: 增加切分两个文本之间的内容，即第一个文本的最大相似度切片开始，至第二个文本相似度最大的结束。


class TextPrepareBase(BaseModel):
    """"""

    @classmethod
    def validate_keywords(cls, keywords: Union[str, List[str]]) -> None:
        """ 验证关键词 """
        for keyword in keywords:
            if len(keyword) == 0:
                raise ValueError("keyword can't be empty!")

    @classmethod
    def find_keyword_index(cls, string: str, keyword: str) -> List[int]:
        """ 找到关键词在原文中的位置 """
        idx = []
        index = string.find(keyword)
        idx.append(index)
        while index != -1:
            index = string.find(keyword, index + 1)
            idx.append(index)
        return idx

    @classmethod
    def keyword_top_n_segments_idx(cls, emb, keywords, segments, top_n=1) -> List[List[int]]:
        """"""
        segments_vector = np.array(emb(data=segments))
        keywords_vector = np.array(emb(data=keywords))
        metrix = cosine_similarity(
            keywords_vector,
            segments_vector.T
        )
        top_n_idx = similarity_topn_idx(
            cosine_matrix=metrix,
            axis=1,
            top_n=top_n,
            ascending=False,
        )
        return top_n_idx

    @classmethod
    def split_string(cls, string: str, k: int) -> List[str]:
        """
        对字符串进行分割，依据固定的字符串数量进行分割。
        :param string:
        :param k:
        :return:
        """
        segments = []
        for i in range(0, len(string), k):
            segment = string[i: i + k]
            segments.append(segment)
        return segments

    @classmethod
    def split_string_with_overlap(
            cls,
            string: str,
            chunk_size: int = 512,
            chunk_overlap: int = 20,
    ) -> List[str]:
        """"""
        segments = [string[i: i + chunk_size] for i in
                    range(0, len(string), chunk_size - chunk_overlap)]
        return segments

    @classmethod
    def split_by_pattern(cls, string: str, pattern: str, k: int) -> List[str]:
        """
        依据多种符号进行文本的切割，并限制最大的字符串的长度。
        :param string:
        :param pattern:
        :param k:
        :return:
        """
        segments = re.split(pattern, string)

        new_content = []
        current_segment = ""
        for segment in segments:
            if len(current_segment) + len(segment) <= k:
                current_segment += segment
            else:
                new_content.append(current_segment.strip())
                current_segment = segment
        if current_segment:
            new_content.append(current_segment.strip())
        return new_content

    @classmethod
    def find_keyword_sub_content_by_name(
            cls,
            string: str,
            keywords: Union[str, List[str]],
            k: int = 1000,
    ) -> List[str]:
        """
        在文本中寻找关键词，并按照关键词后的k个字符进行切割，限制最大的字符串长度。
        :param string:
        :param keywords:
        :param k:
        :return:
        """
        segments = []
        cls.validate_keywords(keywords=keywords)
        for keyword in keywords:
            index = string.find(keyword)
            if index != -1:
                segments.append(string[index: index + k])
            else:
                segments.append([])
        return segments

    @classmethod
    def find_keyword_sub_content_by_emb(
            cls,
            string: str,
            emb: Callable,
            keywords: Union[str, List[str]],
            k: int = 1000,
            n: int = 2,
            pattern: str = '\n\n|。'
    ) -> List[str]:
        """"""
        cls.validate_keywords(keywords=keywords)
        segments = cls.split_by_pattern(
            string=string,
            pattern=pattern,
            k=k,
        )

        top_n_idx = cls.keyword_top_n_segments_idx(
            emb=emb, keywords=keywords, segments=segments, top_n=n,
        )
        return ['\n...\n'.join([segments[i] for i in idx]) for idx in top_n_idx]

    @classmethod
    def find_keyword_sub_content_by_max_smi(
            cls,
            string: str,
            emb: Callable,
            keywords: Union[str, List[str]],
            k: int = 1000,
            n: int = 1,
            pattern: str = '\n|。'
    ) -> List[str]:
        """
        TODO: 在找到多个关键词后，第二次计算尾随文本与关键词的相似度，选择最高的内容

        :param string:
        :param emb:
        :param keywords:
        :param k:
        :param n:
        :param pattern:
        :return:
        """
        cls.validate_keywords(keywords=keywords)
        segments = re.split(pattern, string)
        top_n_idx = cls.keyword_top_n_segments_idx(
            emb=emb, keywords=keywords, segments=segments, top_n=n, )
        new_segments = []
        for idx in top_n_idx:
            segment = []
            for i in idx:
                string_starts = cls.find_keyword_index(string=string, keyword=segments[i])
                for string_start in string_starts:
                    segment.append(string[string_start: string_start + k])
            new_segments.append('\n...\n'.join(segment))
        return new_segments

    @classmethod
    def find_keyword_sub_content(
            cls,
            string: str,
            keywords: Union[str, List[str]],
            k: int = 1000,
            n: Optional[int] = 2,
            emb: Optional[Callable] = None,
            by: Literal['name', 'embedding'] = 'name',
            pattern: str = '\n\n|。',
    ) -> List[str]:
        """
        在文本中寻找关键词，并按照关键词后的k个字符进行切割，限制最大的字符串长度。
        :param pattern:
        :param emb:
        :param n:
        :param by:
        :param string:
        :param keywords:
        :param k:
        :return:
        """
        if isinstance(keywords, str):
            keywords = [keywords]
        cls.validate_keywords(keywords=keywords)

        if by == 'name':
            return cls.find_keyword_sub_content_by_name(string, keywords, k)
        elif by == 'embedding' and emb is not None and n is not None:
            return cls.find_keyword_sub_content_by_emb(
                string=string, emb=emb, keywords=keywords,
                k=k, n=n, pattern=pattern)
        elif by == 'max_smi' and emb is not None:
            return cls.find_keyword_sub_content_by_max_smi(
                string=string, emb=emb, keywords=keywords,
                k=k, n=n, pattern=pattern)
        else:
            raise ValueError(f"by must be one of ['name', 'embedding', 'max_smi']")

    @classmethod
    def drop_center_content(
            cls,
            content: str,
            head_tok: int = 500,
            tail_tok: int = 500,
            min_tok: int = 1000,
    ) -> str:
        """"""
        if head_tok + tail_tok > min_tok:
            raise ValueError(
                f"head_tok: {head_tok}, tail_tok: {tail_tok}, min_tok: {min_tok}, new content have overlap text.")

        if len(content) <= min_tok:
            return content
        else:
            if head_tok == 0 and tail_tok == 0:
                new_content = content
            elif head_tok == 0 and tail_tok != 0:
                new_content = content[-tail_tok:]
            elif head_tok != 0 and tail_tok == 0:
                new_content = content[:head_tok]
            else:
                new_content = '\n\n'.join([content[:head_tok], "……", content[-tail_tok:]])
            return new_content

    @classmethod
    def drop_extreme_content(
            cls,
            content: str,
            min_tok: int = 500,
    ) -> str:
        """"""
        if len(content) <= min_tok:
            return content
        else:
            length = len(content)
            start_index = (length - min_tok) // 2
            end_index = start_index + min_tok
            new_content = content[start_index: end_index]
            return new_content


class PolicySupportText(TextPrepareBase):
    """"""
    content: str
    cleaned_content: str = ""
    cleaned_content_length: int = ""

    def clean(self, min_tok=1000):
        """

        :return:
        """
        self.cleaned_content = re.sub('\xa0|\u2002|\u3000|\u2003|\t', '', self.content)
        self.cleaned_content = re.sub('\n+', '\n\n', self.cleaned_content)
        if "附件" in self.cleaned_content and len(self.cleaned_content) > min_tok:
            matches = [item for item in re.finditer('附件', self.cleaned_content)]
            self.cleaned_content = self.cleaned_content[:list(matches)[-1].start()]
        self.cleaned_content_length = len(self.cleaned_content)

    def select_basic_info_content(
            self,
            head_tok: int = 500,
            tail_tok: int = 500,
            min_tok: int = 1000,
            drop_type: Literal['center', 'extreme'] = 'center'
    ) -> str:
        """"""
        if drop_type == 'extreme':
            return self.drop_extreme_content(content=self.cleaned_content, min_tok=min_tok)
        elif drop_type == 'center':
            return self.drop_center_content(
                content=self.cleaned_content, head_tok=head_tok, tail_tok=tail_tok, min_tok=min_tok)

    def select_is_support(
            self,
            min_tok: int = 1000,
            text_block_tok: Optional[int] = None,
            num_block: int = 2,
    ) -> str:
        """
        选取文中的 num_block 个文本块，并判断是否是支持的内容
        :return:
        """
        if text_block_tok is None:
            text_block_tok = min_tok // 2
        if self.cleaned_content_length <= min_tok:
            return self.cleaned_content
        else:
            if self.cleaned_content_length > 2 * min_tok:
                center_start = min_tok // 2
                center_content = self.cleaned_content[center_start: -center_start]
                if len(center_content) > 2 * min_tok:
                    center_content_block = self.split_string(string=self.cleaned_content, k=text_block_tok)

                    if len(center_content_block) - num_block <= 0:
                        center_content_text = ''.join(center_content_block)
                    elif 0 < len(center_content_block) - num_block < 2:
                        center_content_text = ''.join(center_content_block[:num_block])
                    elif len(center_content_block) - num_block >= 2:
                        idx = np.arange(1, len(center_content_block) - 1)
                        rand_idx = np.random.choice(idx, size=num_block, replace=False).tolist()
                        idx_sorted = sorted(rand_idx)
                        center_content_text = '\n……\n'.join([center_content_block[i] for i in idx_sorted])
                    else:
                        raise ValueError(f"num_block: {num_block} error. center_content_block: {center_content_block}.")

                    return center_content_text
                else:
                    return center_content[:min_tok]
            else:
                return self.drop_extreme_content(content=self.cleaned_content, min_tok=min_tok)

    def select_extract_support(
            self,
            min_tok: int = 1000,
            separator: Union[str, List[str]] = '\n\n'
    ) -> List[str]:
        """"""
        if isinstance(separator, list):
            pattern = "|".join(separator)
        else:
            pattern = separator
        return self.split_by_pattern(string=self.cleaned_content, pattern=pattern, k=min_tok)

    def select_project_condition_content(
            self,
            min_tok: int = 1000,
            emb: Optional[Callable] = None,
            keywords: Optional[List[str]] = [],
            pattern: str = '\n|。',
            n: int = 1,
    ) -> List[Dict]:
        """"""
        segments = self.find_keyword_sub_content_by_max_smi(
            string=self.cleaned_content, emb=emb, keywords=keywords,
            k=min_tok, n=n, pattern=pattern
        )
        project_content = []
        for tag, seg in zip(keywords, segments):
            project_content.append({
                "project_name": tag,
                "content": seg,
            })
        return project_content
