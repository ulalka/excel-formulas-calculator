# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.operands import (ErrorOperand, ValueErrorOperand, Operand, SimpleOperand,
                              LinkErrorOperand, CellRangeOperand, CellSetOperand, ZeroDivisionErrorOperand,
                              SingleCellOperand, NotFoundErrorOperand)
from efc.rpn.errors import EFCLinkError
from functools import wraps
from six import string_types, integer_types
from copy import deepcopy
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
            for cell in arg:
                yield cell
        else:
            yield arg


def iter_digits(yield_none, *args):
    for op in iter_elements(*args):
        if op.is_blank:
            if yield_none:
                yield None
        else:
            try:
                yield op.digit
            except:
                pass


def sum_func(*args):
    return sum(iter_digits(False, *args))


def mod_func(op1, op2):
    return op1.digit % op2.digit


def if_func(expr_op, op1, op2):
    return op1 if expr_op.value else op2


def if_error_func(op1, op2):
    return op2 if isinstance(op1, ErrorOperand) else op1


def max_func(*args):
    return max(list(iter_digits(False, *args)) or [0])


def min_func(*args):
    return min(list(iter_digits(False, *args)) or [0])


def left_func(op1, op2):
    return op1.string[:int(op2)]


def right_func(op1, op2):
    return op1.string[-int(op2):]


def mid_func(op1, op2, op3):
    left = int(op2) - 1
    right = left + int(op3)
    return op1.string[left:right]


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
                if not op.is_blank and isinstance(op.value, (integer_types, float))])


def abs_function(a):
    return abs(a.digit)


def match_function(op1, r, match_type=None):
    match_type = 0 if match_type is None else int(match_type)

    expr = op1.any
    idx = None
    if match_type == 1:
        for idx, item in enumerate(r, 1):
            if item.any == expr:
                break
            elif item.any > expr:
                idx -= 1
                break
    elif match_type == -1:
        for idx, item in enumerate(r, 1):
            if item.any > expr:
                break
        else:
            idx = None
    else:
        for idx, item in enumerate(r, 1):
            if item.any == expr:
                break
        else:
            idx = None
    if idx is None:
        raise NotFoundErrorOperand()
    return idx


COUNT_IF_EXPR = re.compile(r'^(?P<symbol><=|>=|<>|>|<|=)(?P<value>.+)$')


def get_check_function(expr):
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
    return check, operand


def countif_function(cells, expr):
    check, operand = get_check_function(expr)
    return len([op for op in cells.value if not op.is_blank and check(op, operand).value])


def ifs_indexes(*args):
    args = iter(args)
    good_indexes = set()
    first_iteration = True
    while True:
        try:
            op = next(args)
        except StopIteration:
            break

        check, expr = get_check_function(next(args))
        for idx, item in enumerate(op, 1):
            if check(item, expr).value:
                if first_iteration:
                    good_indexes.add(idx)
            elif idx in good_indexes:
                good_indexes.remove(idx)
        first_iteration = False
    return good_indexes


def sum_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return sum_func(*[c for idx, c in enumerate(op1, 1) if idx in good_indexes])


def average_function(*args):
    values = list(iter_digits(False, *args))
    return sum(values) / len(values)


def average_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return average_function(*[c for idx, c in enumerate(op1, 1) if idx in good_indexes])


def count_blank_function(cells):
    return len([op for op in iter_elements(cells) if op.is_blank])


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


def vlookup_function(op, rg, column, flag=None):
    first_col = deepcopy(rg)
    first_col.column2 = first_col.column1

    if flag is not None and flag.digit or flag is None:
        idx = match_function(op, first_col, 1)
        if flag.digit and idx != 1 and list(first_col)[idx - 1].value == op.value:
            idx -= 1
    else:
        idx = match_function(op, first_col, 0)
    return SingleCellOperand(row=(rg.row1 or 1) + idx - 1, column=(rg.column1 or 1) + column.digit - 1,
                             ws_name=rg.ws_name, source=rg.source)


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
EXCEL_FUNCTIONS['SUMIFS'] = excel_function(sum_ifs_function)
EXCEL_FUNCTIONS['MOD'] = excel_function(mod_func)
EXCEL_FUNCTIONS['IF'] = excel_function(if_func)
EXCEL_FUNCTIONS['IFERROR'] = excel_function(if_error_func)
EXCEL_FUNCTIONS['MAX'] = excel_function(max_func)
EXCEL_FUNCTIONS['MIN'] = excel_function(min_func)
EXCEL_FUNCTIONS['LEFT'] = excel_function(left_func)
EXCEL_FUNCTIONS['RIGHT'] = excel_function(right_func)
EXCEL_FUNCTIONS['MID'] = excel_function(mid_func)
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
EXCEL_FUNCTIONS['MATCH'] = excel_function(match_function)
EXCEL_FUNCTIONS['AVERAGE'] = excel_function(average_function)
EXCEL_FUNCTIONS['AVERAGEIFS'] = excel_function(average_ifs_function)
EXCEL_FUNCTIONS['VLOOKUP'] = excel_function(vlookup_function)
