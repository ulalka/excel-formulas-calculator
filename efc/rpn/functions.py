# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.errors import OperandLikeError
from efc.utils import to_unicode
import six

if six.PY2:
    str = to_unicode


def add_func(a, b):
    return a + b


def subtract_func(a, b):
    return a - b


def divide_func(a, b):
    v = float(a) / b
    return int(v) if v % 1 == 0 else v


def multiply_func(a, b):
    v = a * b
    return int(v) if v % 1 == 0 else v


def concat_func(a, b):
    if isinstance(a, float) and a % 1 == 0:
        a = int(a)
    if isinstance(b, float) and b % 1 == 0:
        b = int(b)
    return '%s%s' % (a, b)


def exponent_func(a, b):
    return a ** b


def compare_not_eq_func(a, b):
    return a != b


def compare_gte_func(a, b):
    return a >= b


def compare_lte_func(a, b):
    return a <= b


def compare_gt_func(a, b):
    return a > b


def compare_lt_func(a, b):
    return a < b


def compare_eq_func(a, b):
    return a == b


def iter_elements(args):
    for arg in (a for a in args if a):
        if isinstance(arg, list):
            if isinstance(arg[0], list):
                for row in arg:
                    for item in (i for i in row if i):
                        yield item
            else:
                for item in (i for i in arg if i):
                    yield item
        else:
            yield arg


def sum_func(*args):
    return sum(iter_elements(args))


def mod_func(a, b):
    return a % b


def if_func(expr, a, b):
    return a if expr else b


def if_error_func(a, b):
    return b if isinstance(a, OperandLikeError) else a


def max_func(*args):
    return max(list(iter_elements(args)) or [0.0])


def min_func(*args):
    return min(list(iter_elements(args)) or [0.0])


def left_func(a, b):
    return str(a)[:int(b)]


def right_func(a, b):
    return str(a)[-int(b):]


def is_blank_func(a):
    return a is None


def or_function(*args):
    return any(i for i in iter_elements(args) if not isinstance(i, basestring))


def round_function(a, b):
    return round(float(a), int(b))


ARITHMETIC_FUNCTIONS = {
    '+': add_func,
    '-': subtract_func,
    '/': divide_func,
    '*': multiply_func,
    '&': concat_func,
    '^': exponent_func,
    '<>': compare_not_eq_func,
    '>=': compare_gte_func,
    '<=': compare_lte_func,
    '>': compare_gt_func,
    '<': compare_lt_func,
    '=': compare_eq_func,
}

EXCEL_FUNCTIONS = {}
EXCEL_FUNCTIONS.update(ARITHMETIC_FUNCTIONS)

EXCEL_FUNCTIONS['SUM'] = sum_func
EXCEL_FUNCTIONS['MOD'] = mod_func
EXCEL_FUNCTIONS['IF'] = if_func
EXCEL_FUNCTIONS['IFERROR'] = if_error_func
EXCEL_FUNCTIONS['MAX'] = max_func
EXCEL_FUNCTIONS['MIN'] = min_func
EXCEL_FUNCTIONS['LEFT'] = left_func
EXCEL_FUNCTIONS['RIGHT'] = right_func
EXCEL_FUNCTIONS['ISBLANK'] = is_blank_func
EXCEL_FUNCTIONS['OR'] = or_function
EXCEL_FUNCTIONS['ROUND'] = round_function
