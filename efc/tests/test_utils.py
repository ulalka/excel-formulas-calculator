# coding: utf8

from __future__ import unicode_literals, print_function
import unittest
from efc.utils import col_str_to_index


class TestUtils(unittest.TestCase):
    def test_col_str_to_index(self):
        examples = (
            ('A', 1),
            ('C', 3),
            ('Z', 26),
            ('AA', 27),
            ('HPP', 5840),
        )
        for column, result in examples:
            self.assertEqual(col_str_to_index(column), result)
