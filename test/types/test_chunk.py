import time
import unittest
from zlai.types.chat_completion_chunk import *


class TestChunk(unittest.TestCase):
    """"""
    def test_chunk(self):
        """"""
        choice_delta = ChoiceDelta(role="assistant", content="")
        finish_reason = "stop"

        chunk_choice = Choice(finish_reason=finish_reason, index=0, delta=choice_delta)
        chat_completion_chunk = ChatCompletionChunk(
            id="_id", created=int(time.time()), model="self.model_name", choices=[chunk_choice]
        )
        print(chat_completion_chunk)
