import unittest

from .src import DFA


class DFATest(unittest.TestCase):
    def setUp(self):
        self.x = 1

    def do_test(self):
        assert(self.x == 1)

