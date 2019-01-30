# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.errors import OperandLikeError
from efc.utils import u

from six import string_types, integer_types
import re


def digit(v):
    if isinstance(v, string_types):
        v = float(v)
    elif isinstance(v, bool):
        v = int(v)
    elif v is None:
        v = 0
    elif isinstance(v, OperandLikeError):
        raise v
    return v


def string(v):
    if isinstance(v, OperandLikeError):
        raise v
    return u(v)


def digit_or_string(*args):
    for arg in args:
        if isinstance(arg, OperandLikeError):
            raise arg
        else:
            try:
                arg = digit(arg)
            except ValueError:
                arg = u(arg)
        yield arg


def add_func(*args):
    a, b = args if len(args) == 2 else (0, args[0])
    return digit(a) + digit(b)


def subtract_func(*args):
    a, b = args if len(args) == 2 else (0, args[0])
    return digit(a) - digit(b)


def divide_func(a, b):
    return 1.0 * digit(a) / digit(b)


def multiply_func(a, b):
    return digit(a) * digit(b)


def concat_func(a, b):
    if isinstance(a, float) and a % 1 == 0:
        a = int(a)
    if isinstance(b, float) and b % 1 == 0:
        b = int(b)
    return '%s%s' % (a, b)


def exponent_func(a, b):
    return digit(a) ** digit(b)


def compare_not_eq_func(a, b):
    a, b = digit_or_string(a, b)
    return a != b


def compare_gte_func(a, b):
    a, b = digit_or_string(a, b)
    return a >= b


def compare_lte_func(a, b):
    a, b = digit_or_string(a, b)
    return a <= b


def compare_gt_func(a, b):
    a, b = digit_or_string(a, b)
    return a > b


def compare_lt_func(a, b):
    a, b = digit_or_string(a, b)
    return a < b


def compare_eq_func(a, b):
    a, b = digit_or_string(a, b)
    return a == b


def iter_elements(args):
    for arg in args:
        if isinstance(arg, list):
            if arg and isinstance(arg[0], list):
                for row in arg:
                    for item in row:
                        yield item
            else:
                for item in arg:
                    yield item
        else:
            yield arg


def sum_func(*args):
    return sum(i for i in iter_elements(args) if i)


def mod_func(a, b):
    return digit(a) % digit(b)


def if_func(expr, a, b):
    return a if expr else b


def if_error_func(a, b):
    return b if isinstance(a, OperandLikeError) else a


def max_func(*args):
    return max(list(i for i in iter_elements(args) if i) or [0.0])


def min_func(*args):
    return min(list(i for i in iter_elements(args) if i) or [0.0])


def left_func(a, b):
    return string(a)[:int(b)]


def right_func(a, b):
    return string(a)[-int(b):]


def is_blank_func(a):
    return a is None


def or_function(*args):
    return any(i for i in iter_elements(args) if i and not isinstance(i, string_types))


def round_function(a, b):
    return round(digit(a), int(b))


def count_function(*args):
    return len([i for i in iter_elements(args) if i and isinstance(i, (integer_types, float))])


def abs_function(a):
    return abs(digit(a))


COUNT_IF_EXPR = re.compile(r'^(?P<symbol><=|>=|<>|>|<|=)(?P<value>.+)$')


def countif_function(args, expr):
    if isinstance(expr, string_types):
        match = COUNT_IF_EXPR.search(expr)
        if match:
            match = match.groupdict()
            operation = match['symbol']
            operand = match['value']
        else:
            operation = '='
            operand = expr
    else:
        operation = '='
        operand = expr
    check = ARITHMETIC_FUNCTIONS[operation]
    return len([i for i in iter_elements(args) if i and check(i, operand)])


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
EXCEL_FUNCTIONS['COUNT'] = count_function
EXCEL_FUNCTIONS['COUNTIF'] = countif_function
EXCEL_FUNCTIONS['ABS'] = abs_function
