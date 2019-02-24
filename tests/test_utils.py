# coding: utf8

from __future__ import unicode_literals, print_function
from efc.utils import col_str_to_index
import pytest


@pytest.mark.parametrize(
    ['col', 'index'],
    (
            ('A', 1),
            ('C', 3),
            ('Z', 26),
            ('AA', 27),
            ('HPP', 5840),
    )
)
def test_col_str_to_index(col, index):
    assert col_str_to_index(col) == index
