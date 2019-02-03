# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.operands import (ErrorOperand, ValueErrorOperand, Operand, SimpleOperand,
                              LinkErrorOperand, CellRangeOperand, CellSetOperand, ZeroDivisionErrorOperand,
                              SingleCellOperand)
from efc.rpn.errors import EFCLinkError
from functools import wraps
from six import string_types, integer_types
import re

__all__ = ('EXCEL_FUNCTIONS', )


def add_func(*args):
    if len(args) == 2:
        op1, op2 = args
        return op1.digit + op2.digit
    else:
        return args[0].digit


def subtract_func(*args):
    if len(args) == 2:
        op1, op2 = args
        return op1.digit - op2.digit
    else:
        return -args[0].digit


def divide_func(op1, op2):
    return 1.0 * op1.digit / op2.digit


def multiply_func(op1, op2):
    return op1.digit * op2.digit


def concat_func(op1, op2):
    a = op1.value
    b = op2.value
    if isinstance(a, float) and a % 1 == 0:
        a = int(a)
    if isinstance(b, float) and b % 1 == 0:
        b = int(b)
    return '%s%s' % (a, b)


def exponent_func(op1, op2):
    return op1.digit ** op2.digit


def compare_not_eq_func(op1, op2):
    return op1.any != op2.any


def compare_gte_func(op1, op2):
    return op1.any >= op2.any


def compare_lte_func(op1, op2):
    return op1.any <= op2.any


def compare_gt_func(op1, op2):
    return op1.any > op2.any


def compare_lt_func(op1, op2):
    return op1.any < op2.any


def compare_eq_func(op1, op2):
    return op1.any == op2.any


def iter_elements(*args):
    for arg in args:
        if isinstance(arg, (CellRangeOperand, CellSetOperand)):
            for cell in arg.value:
                yield cell
        else:
            yield arg


def sum_func(*args):
    return sum(op.digit for op in iter_elements(*args) if op.value is not None)


def mod_func(op1, op2):
    return op1.digit % op2.digit


def if_func(expr_op, op1, op2):
    return op1 if expr_op.value else op2


def if_error_func(op1, op2):
    return op2 if isinstance(op1, ErrorOperand) else op1


def max_func(*args):
    return max([op.digit for op in iter_elements(*args) if op.value is not None] or [0])


def min_func(*args):
    return min([op.digit for op in iter_elements(*args) if op.value is not None] or [0])


def left_func(op1, op2):
    return str(op1)[:int(op2)]


def right_func(op1, op2):
    return str(op1)[-int(op2):]


def is_blank_func(a):
    return a.value is None


def or_function(*args):
    for op in iter_elements(*args):
        v = op.value
        if v is not None and not isinstance(v, string_types) and v:
            return True
    return False


def round_function(a, b):
    return round(a.digit, int(b))


def round_down_function(a, b):
    base = 10 ** (int(b))
    return a.digit * base // 1 / base


def floor_function(a, multiple):
    multiple = int(multiple)
    return int(a.digit / multiple) * multiple


def count_function(*args):
    return len([op for op in iter_elements(*args)
                if op.value is not None and isinstance(op.value, (integer_types, float))])


def abs_function(a):
    return abs(a.digit)


COUNT_IF_EXPR = re.compile(r'^(?P<symbol><=|>=|<>|>|<|=)(?P<value>.+)$')


def countif_function(cells, expr):
    if isinstance(expr.value, string_types):
        match = COUNT_IF_EXPR.search(expr.value)
        if match:
            match = match.groupdict()
            operation = match['symbol']
            operand = SimpleOperand(match['value'])
        else:
            operation = '='
            operand = expr
    else:
        operation = '='
        operand = expr
    check = ARITHMETIC_FUNCTIONS[operation]
    return len([op for op in cells.value if op.value is not None and check(op, operand).value])


def count_blank_function(cells):
    return len([op for op in iter_elements(cells) if op.value is None])


def offset_function(cell, row_offset, col_offset, height=None, width=None):
    if not isinstance(cell, SingleCellOperand):
        return ValueErrorOperand()

    height = int(height) if height is not None else 1
    width = int(width) if width is not None else 1

    if height == width == 1:
        return SingleCellOperand(row=cell.row + int(row_offset), column=cell.column + int(col_offset),
                                 ws_name=cell.ws_name, source=cell.source)
    else:
        return CellRangeOperand(row1=cell.row + int(row_offset),
                                column1=cell.column + int(col_offset),
                                row2=cell.row + int(row_offset) + height - 1,
                                column2=cell.column + int(col_offset) + width - 1,
                                ws_name=cell.ws_name, source=cell.source)


def excel_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if not isinstance(result, Operand):
                result = SimpleOperand(result)
            return result
        except ErrorOperand as err:
            return err
        except EFCLinkError:
            return LinkErrorOperand()
        except (TypeError, ValueError):
            return ValueErrorOperand()
        except ZeroDivisionError:
            return ZeroDivisionErrorOperand()

    return wrapper


ARITHMETIC_FUNCTIONS = {
    '+': excel_function(add_func),
    '-': excel_function(subtract_func),
    '/': excel_function(divide_func),
    '*': excel_function(multiply_func),
    '&': excel_function(concat_func),
    '^': excel_function(exponent_func),
    '<>': excel_function(compare_not_eq_func),
    '>=': excel_function(compare_gte_func),
    '<=': excel_function(compare_lte_func),
    '>': excel_function(compare_gt_func),
    '<': excel_function(compare_lt_func),
    '=': excel_function(compare_eq_func),
}

EXCEL_FUNCTIONS = {}
EXCEL_FUNCTIONS.update(ARITHMETIC_FUNCTIONS)

EXCEL_FUNCTIONS['SUM'] = excel_function(sum_func)
EXCEL_FUNCTIONS['MOD'] = excel_function(mod_func)
EXCEL_FUNCTIONS['IF'] = excel_function(if_func)
EXCEL_FUNCTIONS['IFERROR'] = excel_function(if_error_func)
EXCEL_FUNCTIONS['MAX'] = excel_function(max_func)
EXCEL_FUNCTIONS['MIN'] = excel_function(min_func)
EXCEL_FUNCTIONS['LEFT'] = excel_function(left_func)
EXCEL_FUNCTIONS['RIGHT'] = excel_function(right_func)
EXCEL_FUNCTIONS['ISBLANK'] = excel_function(is_blank_func)
EXCEL_FUNCTIONS['OR'] = excel_function(or_function)
EXCEL_FUNCTIONS['ROUND'] = excel_function(round_function)
EXCEL_FUNCTIONS['ROUNDDOWN'] = excel_function(round_down_function)
EXCEL_FUNCTIONS['FLOOR'] = excel_function(floor_function)
EXCEL_FUNCTIONS['COUNT'] = excel_function(count_function)
EXCEL_FUNCTIONS['COUNTIF'] = excel_function(countif_function)
EXCEL_FUNCTIONS['COUNTBLANK'] = excel_function(count_blank_function)
EXCEL_FUNCTIONS['ABS'] = excel_function(abs_function)
EXCEL_FUNCTIONS['OFFSET'] = excel_function(offset_function)
