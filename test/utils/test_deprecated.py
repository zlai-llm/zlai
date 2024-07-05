import unittest
from zlai.utils import *


class TestDeprecated(unittest.TestCase):
    """"""

    def test_deprecated(self):
        @deprecated(since='1.0.0', alternative='new_function()')
        def old_function():
            pass

        @deprecated(since='2.5.0', message="%(name)s is no longer recommended. Please use %(alternative)s.",
                    name='legacy_class', alternative='modern_class')
        class LegacyClass:
            pass
        old_function()
        LegacyClass()

        @deprecated(since='2.5.0', removal="2.7.0", alternative='NewClass')
        class OldClass:
            pass

        OldClass()