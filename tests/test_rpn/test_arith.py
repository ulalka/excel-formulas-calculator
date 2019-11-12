# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from efc import get_calculator


@pytest.fixture(scope='module')
def calculate():
    calculator = get_calculator()
    return lambda line: calculator(line, None, None)


@pytest.mark.parametrize(
    ['line', 'result'],
    (
            ('4', 4),
            ('-4', -4),
            ('4 + 4', 8),
            ('-4 + 4', 0),
            ('4 - 2', 2),
            ('4 * 4', 16),
            ('9 ^ 2', 81),
            ('9 / 3', 3),
            ('1 + 2 * 3', 7),
            ('2 * 3 + 1', 7),
            ('2 - (2 - 3)', 3),
            ('2 - (-2 - 3)', 7),
            ('2 - 2 * 8 - 3', -17),
            ('2 - 2 - 3 - 6', -9),
            ('2 - 2 - 3', -3),
            ('2 - 2 + 3', 3),
            ('2 - (2 + 3)', -3),
    )
)
def test_arithmetic(calculate, line, result):
    assert calculate(line).value == result


@pytest.mark.parametrize(
    ['line', 'result'],
    (
            ('4 = 3', False),
            ('4 <> 3', True),
            ('4 > 3', True),
            ('4 >= 4', True),
            ('4 < 3', False),
            ('3 <= 3', True),
            ('4 + 1 > 4', True),
            ('4 > 4 - 3', True),
            ('4 * 2 + 2 <> 4 / 3 - 1', True),

            ('1 > TRUE', False),
            ('1 > FALSE', False),
            ('1 > "1"', False),
            ('"1" > 1', True),

            ('1 = TRUE', False),
            ('1 = FALSE', False),
            ('1 = "1"', False),
            ('"1" = 1', False),

            ('1 < TRUE', True),
            ('1 < FALSE', True),
            ('1 < "1"', True),
            ('"1" < 1', False),
    )
)
def test_compare(calculate, line, result):
    assert calculate(line).value == result


@pytest.mark.parametrize(
    ['line', 'result'],
    (
            ('"test" & "2"', 'test2'),
            ('2 & 3', '23'),
    )
)
def test_concat(calculate, line, result):
    assert calculate(line).value == result
