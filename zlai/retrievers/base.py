from typing import List, Dict, Union
from pydantic import BaseModel
from ..llms import LocalLLMAPI
from ..schema import Message


__all__ = [
    "BaseRetriever",
]


class BaseRetriever:
    """"""
    llm: Union[LocalLLMAPI]
    query: str
    system_message: List[Message]

    def relevant_documents(self, query: str) -> List[Dict]:
        raise NotImplementedError

