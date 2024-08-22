import unittest
from cachetools import cached, TTLCache


@cached(cache=TTLCache(ttl=300, maxsize=2))
def add(a, b):
    return a + b


class TestCache(unittest.TestCase):
    """"""

    def test_(self):
        """"""
        @cached(cache=TTLCache(maxsize=4, ttl=100))
        def load_glm4(model_path, max_memory=None):
            return None, None

        a = load_glm4("/a", tuple(("0", "30GB")))
        print(list(load_glm4.cache))
        b = load_glm4("/b",)
        print(list(load_glm4.cache))
        for item in list(load_glm4.cache):
            print(item[0])

