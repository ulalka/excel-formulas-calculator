# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from efc.utils import col_str_to_index


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
