# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime

import pytest

from efc.utils import col_str_to_index, datetime_to_openxml, parse_date


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
            ('1', datetime(1900, 1, 1)),
            ('2', datetime(1900, 1, 2)),
            ('61', datetime(1900, 3, 1)),
            ('39448', datetime(2008, 1, 1)),
            ('43831.0234', datetime(2020, 1, 1)),
            ('43832', datetime(2020, 1, 2)),
    )
)
def test_parse_date(dt, cleaned_dt):
    assert parse_date(dt) == cleaned_dt


@pytest.mark.parametrize(
    ['dt', 'openxml_dt'],
    (
            (datetime(1900, 1, 1), '1'),
            (datetime(1900, 1, 2), '2'),
            (datetime(1900, 3, 1), '61'),
            (datetime(2008, 1, 1), '39448'),
            (datetime(2020, 1, 1, minute=33, second=41, microsecond=760000), '43831.0234'),
            (datetime(2020, 1, 2), '43832'),
            (datetime(2020, 1, 1, 1, 0, 1), '43831.041678240741'),
    )
)
def test_datetime_to_openxml(dt, openxml_dt):
    assert datetime_to_openxml(dt) == openxml_dt
