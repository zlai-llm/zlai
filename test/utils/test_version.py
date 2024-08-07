import sys
import unittest
from zlai.utils import pkg_config


class TestVersion(unittest.TestCase):
    """"""

    def test_version(self):
        """"""
        print(sys.version_info)
        print(pkg_config.python_version >= (3, 10))
