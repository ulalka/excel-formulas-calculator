# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
from os.path import dirname, join

import pytest
from openpyxl import load_workbook

from efc.interfaces.iopenpyxl import OpenpyxlInterface


@pytest.fixture(scope='function')
def workbook():
    path = join(dirname(__file__), 'fixtures', 'openpyxl.xlsx')
    return load_workbook(path)


@pytest.fixture(scope='function')
def interface(workbook):
    return OpenpyxlInterface(workbook, use_cache=True)


@pytest.mark.parametrize(
    ('cell', 'result'),
    (
            ('A1', 1),
            ('A2', 2),
            ('A3', 3),
            ('A4', 4),
            ('A5', 5),
    )
)
def test_simple_cell_value(cell, result, interface):
    assert interface.calc_cell(cell, 'ws1') == result


@pytest.mark.parametrize(
    ('cell', 'result'),
    (
            ('B1', 2),
            ('B2', 3),
            ('B3', 4),
            ('B4', 5),
            ('B5', 6),
    )
)
def test_simple_formula_value(cell, result, interface):
    assert interface.calc_cell(cell, 'ws1') == result


@pytest.mark.parametrize(
    ('cell', 'result'),
    (
            ('D1', 15),
            ('D2', 20),
            ('D3', 15),
            ('D4', 46),
    )
)
def test_sum_formula_value(cell, result, interface):
    assert interface.calc_cell(cell, 'ws1') == result


@pytest.mark.parametrize(
    ('cell', 'result'),
    (
            ('A7', datetime(2020, 1, 1)),
            ('B7', datetime(2020, 1, 2)),
            ('C7', 1),
    )
)
def test_date_operations_value(cell, result, interface):
    assert interface.calc_cell(cell, 'ws1') == result


@pytest.mark.parametrize(
    ('cell', 'result'),
    (
            ('A8', 'text1'),
            ('B8', 'text2'),
            ('C8', 'text1text2'),
    )
)
def test_test_operations_value(cell, result, interface):
    assert interface.calc_cell(cell, 'ws1') == result


def test_openpyxl_cache_enabled(workbook, interface):
    assert interface.calc_cell('B1', 'ws1') == 2
    workbook['ws1']['A1'].value = 3
    assert interface.calc_cell('B1', 'ws1') == 2  # value from cache
    interface.clear_cache()
    assert interface.calc_cell('B1', 'ws1') == 4


def test_openpyxl_cache_disabled(workbook):
    interface = OpenpyxlInterface(workbook, use_cache=False)
    assert interface.calc_cell('B1', 'ws1') == 2
    workbook['ws1']['A1'].value = 3
    assert interface.calc_cell('B1', 'ws1') == 4
