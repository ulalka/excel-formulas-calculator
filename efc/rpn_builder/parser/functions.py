# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re

from six import integer_types, string_types

from efc.rpn_builder.parser.operands import (BadReference, CellRangeOperand, CellSetOperand, ErrorOperand,
                                             NotFoundErrorOperand, RPNOperand, SimpleOperand, SingleCellOperand,
                                             ValueErrorOperand)
from efc.utils import is_float

__all__ = ('EXCEL_FUNCTIONS',)


def _get_type_id(obj):
    if isinstance(obj, bool):
        return 2
    elif isinstance(obj, string_types):
        return 1
    return 0


def type_mixin(a, b):
    if a is None:
        a = '' if isinstance(b, string_types) else 0
    if b is None:
        b = '' if isinstance(a, string_types) else 0
    return (_get_type_id(a), a), (_get_type_id(b), b)


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
    return op1.digit / op2.digit


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
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 != op2


def compare_gte_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 >= op2


def compare_lte_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 <= op2


def compare_gt_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 > op2


def compare_lt_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 < op2


def compare_eq_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 == op2


def iter_elements(*args):
    for arg in args:
        if isinstance(arg, RPNOperand):
            arg = arg.evaluated_value

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


def if_func(expr_op, op1, op2=None):
    if op2 is None:
        op2 = False
    return op1 if expr_op.value else op2


def if_error_func(op1, op2):
    if isinstance(op1, RPNOperand):
        op1 = op1.evaluated_value
    return op2 if isinstance(op1, ErrorOperand) else op1


def max_func(*args):
    return max(list(iter_digits(False, *args)) or [0])


def min_func(*args):
    return min(list(iter_digits(False, *args)) or [0])


def left_func(op1, op2=1):
    return op1.string[:int(op2)]


def right_func(op1, op2=1):
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


def and_function(*args):
    for op in iter_elements(*args):
        v = op.value
        if v is not None and not isinstance(v, string_types) and not v:
            return False
    return True


def not_func(op):
    return not op.value


def small_function(r, op):
    items = sorted(iter_digits(False, r))
    index = int(op) - 1
    try:
        return items[index]
    except IndexError:
        return ValueErrorOperand()


def large_function(r, op):
    items = sorted(iter_digits(False, r), reverse=True)
    index = int(op) - 1
    try:
        return items[index]
    except IndexError:
        return ValueErrorOperand()


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

    expr = op1.value
    idx = None
    if match_type == 1:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a == b:
                break
            elif a > b:
                idx -= 1
                break
    elif match_type == -1:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a > b:
                break
        else:
            idx = None
    else:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a == b:
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
            operand = match['value']
        else:
            operation = '='
            operand = expr.value
    else:
        operation = '='
        operand = expr.value

    if is_float(operand):
        operand = float(operand)

    check = ARITHMETIC_FUNCTIONS[operation]
    return check, SimpleOperand(operand)


def countif_function(cells, expr):
    check, operand = get_check_function(expr)
    return len([op for op in cells.value if not op.is_blank and check(op, operand)])


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
            if check(item, expr):
                if first_iteration:
                    good_indexes.add(idx)
            elif idx in good_indexes:
                good_indexes.remove(idx)
        first_iteration = False
    return good_indexes


def sum_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return sum_func(*[c for idx, c in enumerate(op1, 1) if idx in good_indexes])


def concatenate(*args):
    return ''.join(i.string for i in iter_elements(*args) if not i.is_blank)


def average_function(*args):
    values = list(iter_digits(False, *args))
    return sum(values) / len(values)


def average_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return average_function(*[c for idx, c in enumerate(op1, 1) if idx in good_indexes])


def count_blank_function(cells):
    return len([op for op in iter_elements(cells) if op.is_blank])


def count_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return count_function(*[c for idx, c in enumerate(op1, 1) if idx in good_indexes])


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
    first_col = rg.offset()
    first_col.column2 = first_col.column1

    if flag is not None and flag.digit or flag is None:
        idx = match_function(op, first_col, 1)
        if flag is not None and flag.digit and idx != 1:
            a, b = type_mixin(list(first_col)[idx - 1].value, op.value)
            if a == b:
                idx -= 1
    else:
        idx = match_function(op, first_col, 0)
    return SingleCellOperand(row=(rg.row1 or 1) + idx - 1, column=(rg.column1 or 1) + column.digit - 1,
                             ws_name=rg.ws_name, source=rg.source)


def index_function(rg, row, column=None):
    if rg.row1 != rg.row2 and rg.column1 != rg.column2:
        rg_size = 2
    else:
        rg_size = 1

    row = row.digit
    if column is not None:
        column = column.digit

    if row <= 0 or column is not None and column <= 0:
        return BadReference()

    if rg_size == 1 and column is not None or rg_size == 2 and column is None:
        return BadReference()

    if rg_size == 1:
        if rg.row1 == rg.row2:
            if rg.column2 - rg.column1 + 1 < row:
                return BadReference()
            return SingleCellOperand(rg.row1, rg.column1 - 1 + row, ws_name=rg.ws_name, source=rg.source)
        else:
            if rg.row2 - rg.row1 + 1 < row:
                return BadReference()
            return SingleCellOperand(rg.row1 - 1 + row, rg.column1, ws_name=rg.ws_name, source=rg.source)
    else:
        if rg.row2 - rg.row1 + 1 < row or rg.column2 - rg.column1 + 1 < column:
            return BadReference()
        return SingleCellOperand(rg.row1 - 1 + row, rg.column1 - 1 + column, ws_name=rg.ws_name, source=rg.source)


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
EXCEL_FUNCTIONS['SUMIFS'] = sum_ifs_function
EXCEL_FUNCTIONS['MOD'] = mod_func
EXCEL_FUNCTIONS['IF'] = if_func
EXCEL_FUNCTIONS['IFERROR'] = if_error_func
EXCEL_FUNCTIONS['MAX'] = max_func
EXCEL_FUNCTIONS['MIN'] = min_func
EXCEL_FUNCTIONS['LEFT'] = left_func
EXCEL_FUNCTIONS['RIGHT'] = right_func
EXCEL_FUNCTIONS['MID'] = mid_func
EXCEL_FUNCTIONS['ISBLANK'] = is_blank_func
EXCEL_FUNCTIONS['OR'] = or_function
EXCEL_FUNCTIONS['AND'] = and_function
EXCEL_FUNCTIONS['NOT'] = not_func
EXCEL_FUNCTIONS['ROUND'] = round_function
EXCEL_FUNCTIONS['ROUNDDOWN'] = round_down_function
EXCEL_FUNCTIONS['FLOOR'] = floor_function
EXCEL_FUNCTIONS['COUNT'] = count_function
EXCEL_FUNCTIONS['COUNTIF'] = countif_function
EXCEL_FUNCTIONS['COUNTBLANK'] = count_blank_function
EXCEL_FUNCTIONS['ABS'] = abs_function
EXCEL_FUNCTIONS['OFFSET'] = offset_function
EXCEL_FUNCTIONS['MATCH'] = match_function
EXCEL_FUNCTIONS['AVERAGE'] = average_function
EXCEL_FUNCTIONS['AVERAGEIFS'] = average_ifs_function
EXCEL_FUNCTIONS['VLOOKUP'] = vlookup_function
EXCEL_FUNCTIONS['SMALL'] = small_function
EXCEL_FUNCTIONS['LARGE'] = large_function
EXCEL_FUNCTIONS['COUNTIFS'] = count_ifs_function
EXCEL_FUNCTIONS['CONCATENATE'] = concatenate
EXCEL_FUNCTIONS['INDEX'] = index_function
