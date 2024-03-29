# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from efc.rpn_builder.parser.operands import BLANK_OPERAND, WorksheetNotExist
from .mock import ExcelMock, get_calculator


@pytest.fixture(scope='session')
def calc():
    source = ExcelMock()
    calculator = get_calculator()
    return lambda line, ws_name: calculator(line, ws_name, source)


def test_cell_address(calc):
    assert calc('A3', 'Sheet 1').value == 4
    assert calc('C1', 'Sheet 1').value == 18

    assert calc('B100', 'Yet another sheet').value == 2
    assert calc('AA104', 'Yet another sheet').value == 45

    with pytest.raises(WorksheetNotExist):
        calc('F104', 'Some error ws').value

    assert calc('Sheet4!A3', 'Yet another sheet').value == 4
    assert calc('\'Sheet 1\'!C1', 'Yet another sheet').value == 18

    # test arith with address
    assert calc('A3 + 3', 'Sheet 1').value == 7
    assert calc('C1 / 9', 'Sheet 1').value == 2

    assert calc('Sheet4!A3 ^ 2', 'Yet another sheet').value == 16
    assert calc('\'Sheet 1\'!C1 - 4 - 1', 'Yet another sheet').value == 13

    result = calc('Sheet4!A1:B3', 'Yet another sheet')
    assert [c.value for c in result.value] == [13, 16, 13, 16, 4, 2]

    assert calc('Sheet4!test', 'Yet another sheet').value == 16
    assert calc('SUM(Sheet4!test2)', 'Yet another sheet').value == 34
    assert calc('SUM([0]Sheet4!test2)', 'Yet another sheet').value == 34


def test_single_cell_cache():
    # Cache disabled
    source = ExcelMock(use_cache=False)
    calculator = get_calculator()

    op1 = calculator('A3', 'Sheet 1', source)
    op2 = calculator('A3', 'Sheet 1', source)

    assert op1 is not op2

    # Cache enabled
    source = ExcelMock(use_cache=True)
    op1 = calculator('A3', 'Sheet 1', source)
    op2 = calculator('A3', 'Sheet 1', source)

    assert op1 is op2

    # New cache value for A3
    source._caches.clear()
    op2 = calculator('A3', 'Sheet 1', source)
    assert op1 is not op2

    # New cache value for A3
    source._caches.remove_cell('Sheet 1', 3, 1)
    op3 = calculator('A3', 'Sheet 1', source)
    assert op2 is not op3

    # Test blank operand
    r = list(calculator('A99:A105', 'Yet another sheet', source))
    assert r[0] is BLANK_OPERAND
    assert r[1] is not BLANK_OPERAND
    assert r[2] is not BLANK_OPERAND
    assert r[3] is not BLANK_OPERAND
    assert r[4] is not BLANK_OPERAND
    assert r[5] is not BLANK_OPERAND
    assert r[6] is BLANK_OPERAND

