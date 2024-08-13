import unittest
from pydantic import BaseModel, Field
from typing import List, Literal


class TestImageGenerateConfig(unittest.TestCase):
    def test_image_generate_config(self):
        class Embedding(BaseModel):
            embedding: List[float]
            """The embedding vector, which is a list of floats.

            The length of vector depends on the model as listed in the
            [embedding guide](https://platform.openai.com/docs/guides/embeddings).
            """

            index: int
            """The index of the embedding in the list of embeddings."""

            object: Literal["embedding"] = Field(default="embedding")
            """The object type, which is always "embedding"."""

        vectors = [[1, 1,], [2., 2]]

        [Embedding(e) for i, vector in enumerate(vectors)]
