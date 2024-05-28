import re
from typing import Union, List, Optional


__all__ = ["TextSplit"]



class TextSplit:
    """ For text split. """
    drop_words: Union[str, List[str]] = r" "
    drop_punctuation: Union[str, List[str]] = r"。|，|、|：|；|\.|,|;|:"
    drop_mark: Union[str, List[str]] = r"\n"
    user_dict_path: Optional[str] = None
    stop_words_path: Optional[str] = None
    user_dict: Optional[List[str]] = None
    stop_words: Optional[List[str]] = None

    def __init__(
            self,
            drop_words: Union[str, List[str]] = r" ",
            drop_punctuation: Union[str, List[str]] = r"。|，|、|：|；|\.|,|;|:",
            drop_mark: Union[str, List[str]] = r"\n",
            user_dict_path: Optional[str] = None,
            stop_words_path: Optional[str] = None,
            user_dict: Optional[List[str]] = None,
            stop_words: Optional[List[str]] = None,
    ):
        """"""
        self.drop_words = drop_words
        self.drop_punctuation = drop_punctuation
        self.drop_mark = drop_mark
        self.user_dict_path = user_dict_path
        self.user_dict = user_dict
        self.stop_words_path = stop_words_path
        self.stop_words = stop_words

    @classmethod
    def _trans_list_pattern(cls, patterns: Union[List[str]]) -> str:
        """"""
        if isinstance(patterns, (list, tuple)):
            str_patterns = '|'.join(patterns)
        elif isinstance(patterns, str):
            str_patterns = patterns
        else:
            raise ValueError("The type of patterns should be str or list.")
        return str_patterns

    def _mapping_word(self, word: str) -> str:
        """"""
        self.drop_words = self._trans_list_pattern(self.drop_words)
        self.drop_punctuation = self._trans_list_pattern(self.drop_punctuation)
        self.drop_mark = self._trans_list_pattern(self.drop_mark)

        pattern = '|'.join([self.drop_words, self.drop_punctuation, self.drop_mark])
        word = re.sub(pattern=pattern, repl='', string=word)
        return word

    def jieba_cut(
            self,
            string: str,
            cut_all: bool = False,
            use_paddle: bool = True,
            HMM: bool = True,
    ) -> List[str]:
        """"""
        try:
            import jieba, logging
            jieba.setLogLevel(log_level=logging.WARNING)
            if self.user_dict_path is not None:
                jieba.load_userdict(self.user_dict_path)
            if self.user_dict is not None:
                [jieba.add_word(word) for word in self.user_dict]
            if self.stop_words is not None:
                [jieba.del_word(word) for word in self.stop_words]
            if self.stop_words_path is not None:
                import jieba.analyse
                jieba.analyse.set_stop_words(self.stop_words_path)
        except ImportError:
            raise ImportError("Please install jieba first.")
        segments = jieba.cut(string, cut_all=cut_all, use_paddle=use_paddle, HMM=HMM)
        segments = list(map(self._mapping_word, segments))
        segments = [item for item in segments if len(item) > 0]
        return segments
