import subprocess
from typing import Any, Annotated, List

from ..llms import TypeLLM
from ..embedding import Embedding
from ..schema import Message
from .base import AgentMixin


__all__ = [
    "get_shell"
]


def get_shell(
        query: Annotated[str, 'The command should run in Linux shell', True],
) -> str:
    """
       Use shell to run command
    """
    if not isinstance(query, str):
        raise TypeError("Command must be a string")
    try:
        result = subprocess.run(query, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


class Shell(AgentMixin):
    """"""

    def __init__(self):
        """"""

    def __call__(self, *args, **kwargs):
        """"""

    def _make_messages(self, **kwargs: Any) -> List[Message]:
        """"""
        return []

    def generate(
            self,
            query: str,
            *args: Any,
            **kwargs: Any
    ) -> str:
        """"""
        return ""
