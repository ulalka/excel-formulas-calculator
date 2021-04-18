# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from efc import get_calculator
from efc.rpn_builder.parser.operands import BadReference, NumErrorOperand
from .mock import ExcelMock


@pytest.fixture(scope='session')
def calc():
    source = ExcelMock()
    calculator = get_calculator()
    return lambda line, ws_name: calculator(line, ws_name, source)


def test_SUM(calc):
    assert calc('SUM(Sheet4!A1:B3)', 'Yet another sheet').value == 64
    assert calc('SUM([0]Sheet4!A1:B3)', 'Yet another sheet').value == 64
    assert calc('SUM(Sheet4!A1:B3) + 1', 'Yet another sheet').value == 65
    assert calc('SUM(Sheet4!A1:B3,A2:B3)', 'Sheet4').value == 99
    assert calc('SUM(Sheet4!A1:B3,SUM(A3:B3))', 'Sheet4').value == 70


def test_SUMIFS(calc):
    assert calc('SUMIFS(Sheet4!A1:B3,Sheet4!A1:B3,">4")', 'Yet another sheet').value == 58
    assert calc('SUMIFS(Sheet4!A1:B3,Sheet4!A1:B3,"13")', 'Yet another sheet').value == 26


def test_SUMIF(calc):
    assert calc('SUMIF(Sheet4!A1:B3,">4",Sheet4!A1:B3)', 'Yet another sheet').value == 58
    assert calc('SUMIF(Sheet4!A1:B3,"13",Sheet4!A1:B3)', 'Yet another sheet').value == 26


def test_MOD(calc):
    assert calc('MOD(\'Sheet 1\'!B3,4)', 'Yet another sheet').value == 2
    assert calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!C3)', 'Yet another sheet').value == 4
    assert calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!B3 * 2)', 'Yet another sheet').value == 0


def test_IF(calc):
    assert calc('IF(2>1,1,2)', 'Yet another sheet').value == 1
    assert calc('IF(TRUE,1,2)', 'Yet another sheet').value == 1
    assert calc('IF(FALSE,1,2)', 'Yet another sheet').value == 2
    assert calc('IF(TRUE,1,2 ** 5)', 'Yet another sheet').value == 1
    assert calc('IF(\'Sheet 1\'!A3 = 4,\'Sheet 1\'!C3, 0)', 'Yet another sheet').value == 8


def test_IFERROR(calc):
    assert calc('IFERROR(5/0,1)', 'Yet another sheet').value == 1
    assert calc('IFERROR(5+6, 0)', 'Yet another sheet').value == 11


def test_MAX(calc):
    assert calc('MAX(Sheet4!A1:B3)', 'Yet another sheet').value == 16
    assert calc('MAX(Sheet4!A1:B3,100)', 'Yet another sheet').value == 100


def test_MIN(calc):
    assert calc('MIN(Sheet4!A1:B3)', 'Yet another sheet').value == 2
    assert calc('MIN(Sheet4!A1:B3,1)', 'Yet another sheet').value == 1


def test_LEFT(calc):
    assert calc('LEFT("test", 2)', 'Yet another sheet').value == 'te'


def test_RIGHT(calc):
    assert calc('RIGHT("test", 2)', 'Yet another sheet').value == 'st'


def test_MID(calc):
    assert calc('MID("hello",2,2)', 'Sheet 1').value == 'el'


def test_ISBLANK(calc):
    assert calc('ISBLANK("test")', 'Yet another sheet').value is False
    assert calc('ISBLANK("")', 'Yet another sheet').value is False
    assert calc('ISBLANK(Sheet4!AA1)', 'Yet another sheet').value is True


def test_OR(calc):
    assert calc('OR(0,0,0,TRUE)', 'Yet another sheet').value is True
    assert calc('OR(FALSE, 0)', 'Yet another sheet').value is False
    assert calc('OR(FALSE, 0 + 2)', 'Yet another sheet').value is True


def test_AND(calc):
    assert calc('AND(1,1,1,TRUE)', 'Yet another sheet').value is True
    assert calc('AND(FALSE, 0)', 'Yet another sheet').value is False
    assert calc('AND(TRUE, 0 + 2)', 'Yet another sheet').value is True


def test_not(calc):
    assert calc('NOT(1)', 'Yet another sheet').value is False
    assert calc('NOT(0)', 'Yet another sheet').value is True
    assert calc('NOT(123)', 'Yet another sheet').value is False
    assert calc('NOT(TRUE)', 'Yet another sheet').value is False
    assert calc('NOT(FALSE)', 'Yet another sheet').value is True
    assert calc('NOT(A1)', 'Yet another sheet').value is True
    assert calc('NOT(A1)', 'Sheet4').value is False
    assert calc('NOT("")', 'Yet another sheet').value is True
    assert calc('NOT(NOT(""))', 'Yet another sheet').value is False


def test_ROUND(calc):
    assert calc('ROUND(2.3456, 1)', 'Yet another sheet').value == 2.3
    assert calc('ROUND(2, 2)', 'Yet another sheet').value == 2.0
    assert calc('ROUND("2.34567", 2)', 'Yet another sheet').value == 2.35


def test_ROUNDDOWN(calc):
    assert calc('ROUNDDOWN(1.345,0)', 'Sheet 1').value == 1.0
    assert calc('ROUNDDOWN(1.345,1)', 'Sheet 1').value == 1.3
    assert calc('ROUNDDOWN(1.345,2)', 'Sheet 1').value == 1.34


def test_FLOOR(calc):
    assert calc('FLOOR(10,3)', 'Sheet 1').value == 9
    assert calc('FLOOR(16,7)', 'Sheet 1').value == 14
    assert calc('FLOOR(26,13)', 'Sheet 1').value == 26


def test_COUNT(calc):
    assert calc('COUNT(1.3456, 1, "test")', 'Yet another sheet').value == 2
    assert calc('COUNT(A1:C4)', 'Sheet 1').value == 6


def test_COUNTIF(calc):
    assert calc('COUNTIF(A1:C4, ">4")', 'Sheet 1').value == 4
    assert calc('COUNTIF(A1:C4, "13")', 'Sheet4').value == 2


def test_COUNTBLANK(calc):
    assert calc('COUNTBLANK(A1:C4)', 'Sheet 1').value == 6
    assert calc('COUNTBLANK(A1:B4)', 'Sheet4').value == 2


def test_ABS(calc):
    assert calc('ABS(1.32)', 'Sheet 1').value == 1.32
    assert calc('ABS(-42)', 'Sheet4').value == 42


def test_OFFSET(calc):
    assert calc('OFFSET(A1,2,1)', 'Sheet 1').value == 2
    assert calc('OFFSET(A1,2,1,1)', 'Sheet 1').value == 2
    assert calc('OFFSET(A1,B3,1)', 'Sheet 1').value == 2
    assert calc('SUM(OFFSET(A1,2,1,1,2))', 'Sheet 1').value == 10


def test_MATCH(calc):
    assert calc('MATCH(13,Sheet4!A1:A3)', 'Yet another sheet').value == 1


def test_AVERAGE(calc):
    assert calc('AVERAGE(Sheet4!A1:B3)', 'Yet another sheet').value == 64 / 6
    assert calc('AVERAGEIFS(Sheet4!A1:B3,Sheet4!A1:B3,"13")', 'Yet another sheet').value == 13


def test_AVERAGEIFS(calc):
    assert calc('AVERAGEIFS(Sheet4!A1:B3,Sheet4!A1:B3,"13")', 'Yet another sheet').value == 13


def test_VLOOKUP(calc):
    assert calc('VLOOKUP(13,Sheet4!A1:B3,2)', 'Yet another sheet').value == 16


def test_SMALL(calc):
    assert calc('SMALL(Sheet4!A1:B3,1)', 'Yet another sheet').value == 2
    assert calc('SMALL(Sheet4!A1:B3,2)', 'Yet another sheet').value == 4
    assert calc('SMALL(Sheet4!A1:B3,4)', 'Yet another sheet').value == 13


def test_LARGE(calc):
    assert calc('LARGE(Sheet4!A1:B3,1)', 'Yet another sheet').value == 16
    assert calc('LARGE(Sheet4!A1:B3,2)', 'Yet another sheet').value == 16
    assert calc('LARGE(Sheet4!A1:B3,4)', 'Yet another sheet').value == 13


def test_COUNTIFS(calc):
    assert calc('COUNTIFS(Sheet4!A1:B3,Sheet4!A1:B3,">4")', 'Yet another sheet').value == 4
    assert calc('COUNTIFS(Sheet4!A1:B3,Sheet4!A1:B3,"13")', 'Yet another sheet').value == 2


def test_COUNTA(calc):
    assert calc('COUNTA(Sheet4!A1:B4)', 'Yet another sheet').value == 6
    assert calc('COUNTA(Sheet5!A1:B4)', 'Yet another sheet').value == 5


def test_CONCATENATE(calc):
    assert calc('CONCATENATE(Sheet4!A1,Sheet4!B3,"13")', 'Yet another sheet').value == '13213'
    assert calc('CONCATENATE("",Sheet4!B3,TRUE)', 'Yet another sheet').value == '2TRUE'


def test_INDEX(calc):
    assert calc('INDEX(Sheet4!A1:A3,1)', 'Yet another sheet').value == 13  # A1
    assert calc('INDEX(Sheet4!A1:B3,1,2)', 'Yet another sheet').value == 16  # B1
    assert calc('INDEX(Sheet4!A1:A3,3)', 'Yet another sheet').value == 4  # A3
    assert calc('INDEX(Sheet4!A2:A3,2)', 'Yet another sheet').value == 4  # A3

    assert calc('INDEX(Sheet4!A:A,3)', 'Yet another sheet').value == 4  # A3
    assert calc('INDEX(Sheet4!A:A,3,1)', 'Yet another sheet').value == 4  # A3
    assert calc('INDEX(Sheet4!3:3,1,1)', 'Yet another sheet').value == 4  # A3
    assert calc('INDEX(Sheet4!3:3,1,2)', 'Yet another sheet').value == 2  # B3

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:A3,100,1)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:A3,1,100)', 'Yet another sheet').value

    assert calc('INDEX(Sheet4!A1:C3,1,1)', 'Yet another sheet').value == 13
    assert calc('INDEX(Sheet4!A1:C3,1,3)', 'Yet another sheet').value == 18

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:C3,1)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:C3,100,1)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:C3,1,100)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:C3,0,100)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A1:C3,1,0)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!A:A,3,2)', 'Yet another sheet').value

    with pytest.raises(BadReference):
        assert calc('INDEX(Sheet4!1:1,2)', 'Yet another sheet').value


def test_SUBSTITUTE(calc):
    assert calc('SUBSTITUTE("123123123","1","22")', 'Yet another sheet').value == '222322232223'
    assert calc('SUBSTITUTE("123123123","1","22", 2)', 'Yet another sheet').value == '22232223123'
    assert calc('SUBSTITUTE("123123123","1","22", -1)', 'Yet another sheet').value == '222322232223'


def test_TRIM(calc):
    assert calc('TRIM(1)', 'Yet another sheet').value == '1'
    assert calc('TRIM(0)', 'Yet another sheet').value == '0'
    assert calc('TRIM("1")', 'Yet another sheet').value == '1'
    assert calc('TRIM(" 1 ")', 'Yet another sheet').value == '1'
    assert calc('TRIM(" 1 1 ")', 'Yet another sheet').value == '1 1'
    assert calc('TRIM(" 1      1 ")', 'Yet another sheet').value == '1 1'


def test_LEN(calc):
    assert calc('LEN(1)', 'Yet another sheet').value == 1
    assert calc('LEN(0)', 'Yet another sheet').value == 1
    assert calc('LEN("1")', 'Yet another sheet').value == 1
    assert calc('LEN(" 1 ")', 'Yet another sheet').value == 3


def test_YEARFRAC(calc):
    with pytest.raises(NumErrorOperand):
        assert calc('YEARFRAC(1, 2, 5)', 'Yet another sheet').value

    # 30U/360
    assert calc('YEARFRAC(43159, 43160)', 'Yet another sheet').value == 1 / 360
    assert calc('YEARFRAC(43405, 43465, 0)', 'Yet another sheet').value == 60 / 360
    assert calc('YEARFRAC(43889, 43890, 0)', 'Yet another sheet').value == 1 / 360
    assert calc('YEARFRAC(43889, 43891, 0)', 'Yet another sheet').value == 3 / 360

    # Actual/Actual
    assert calc('YEARFRAC(43889, 43890, 1)', 'Yet another sheet').value == 1 / 366
    assert calc('YEARFRAC(43889, 43891, 1)', 'Yet another sheet').value == 2 / 366
    assert calc('YEARFRAC(43523, 43524, 1)', 'Yet another sheet').value == 1 / 365
    assert calc('YEARFRAC(43523, 43525, 1)', 'Yet another sheet').value == 2 / 365

    # Actual/360
    assert calc('YEARFRAC(43889, 43890, 2)', 'Yet another sheet').value == 1 / 360
    assert calc('YEARFRAC(43889, 43891, 2)', 'Yet another sheet').value == 2 / 360
    assert calc('YEARFRAC(43523, 43524, 2)', 'Yet another sheet').value == 1 / 360
    assert calc('YEARFRAC(43523, 43525, 2)', 'Yet another sheet').value == 2 / 360

    # Actual/365
    assert calc('YEARFRAC(43889, 43890, 3)', 'Yet another sheet').value == 1 / 365
    assert calc('YEARFRAC(43889, 43891, 3)', 'Yet another sheet').value == 2 / 365
    assert calc('YEARFRAC(43523, 43524, 3)', 'Yet another sheet').value == 1 / 365
    assert calc('YEARFRAC(43523, 43525, 3)', 'Yet another sheet').value == 2 / 365

    # 30E/360
    assert calc('YEARFRAC(43159, 43160, 4)', 'Yet another sheet').value == 3 / 360
    assert calc('YEARFRAC(43405, 43465, 4)', 'Yet another sheet').value == 59 / 360
    assert calc('YEARFRAC(43889, 43890, 4)', 'Yet another sheet').value == 1 / 360
    assert calc('YEARFRAC(43889, 43891, 4)', 'Yet another sheet').value == 3 / 360
