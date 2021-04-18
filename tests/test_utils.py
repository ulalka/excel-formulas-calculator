# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date

import pytest

from efc.utils import col_str_to_index, parse_date


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


@pytest.mark.parametrize(
    ['dt', 'cleaned_dt'],
    (
            ('1', date(1900, 1, 1)),
            ('2', date(1900, 1, 2)),
            ('61', date(1900, 3, 1)),
            ('39448', date(2008, 1, 1)),
            ('43831.0234', date(2020, 1, 1)),
            ('43832', date(2020, 1, 2)),
    )
)
def test_parse_date(dt, cleaned_dt):
    assert parse_date(dt) == cleaned_dt
