from typing import List, Dict, Union
from pydantic import BaseModel
from ..llms import LocalCompletion
from ..schema import Message


__all__ = [
    "BaseRetriever",
]


class BaseRetriever:
    """"""
    llm: Union[LocalCompletion]
    query: str
    system_message: List[Message]

    def relevant_documents(self, query: str) -> List[Dict]:
        raise NotImplementedError

