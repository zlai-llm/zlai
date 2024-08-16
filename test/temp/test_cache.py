import unittest
from cachetools import cached, TTLCache


@cached(cache=TTLCache(ttl=300, maxsize=2))
def add(a, b):
    return a + b


class TestCache(unittest.TestCase):
    """"""

    def test_(self):
        """"""
        print(add.cache)
        c = add(1, 1)
        c = add(2, 1)
        print(list(add.cache))
        add.cache.pop((1, 1))
        print(list(add.cache))

