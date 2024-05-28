import re
from typing import List, Optional
from pydantic import BaseModel


__all__ = [
    "TextClean"
]


class TextClean:
    """"""
    @classmethod
    def drop_brackets(
            cls,
            string: str,
            pattern: Optional[str] = None,
            repl: Optional[str] = "",
            keywords: Optional[List[str]] = None,
    ) -> str:
        """"""
        if keywords is None:
            keywords = ["不包括", "不包含", "不含", "不涉及", "除外", "剔除", "以外"]
        if pattern is None:
            pattern = r'[（\(].*?(' + '|'.join(map(re.escape, keywords)) + r').*?[）\)]'
        new_string = re.sub(pattern, repl, string)
        return new_string

    @classmethod
    def clean(
            cls,
            string: str,
    ) -> str:
        """"""
        string = re.sub('\xa0|\u2002|\u3000|\u2003|\t', '', string)
        string = re.sub('\n+', '\n\n', string)
        return string
