# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn_builder.parser.operands import (ErrorOperand, ValueErrorOperand, OperandLikeObject, SimpleOperand,
                                             LinkErrorOperand, ZeroDivisionErrorOperand, FunctionNotSupported)
from efc.rpn_builder.errors import EFCLinkError
from efc.rpn_builder.parser import functions
from functools import wraps


def excel_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if not isinstance(result, OperandLikeObject):
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
    '+': functions.add_func,
    '-': functions.subtract_func,
    '/': functions.divide_func,
    '*': functions.multiply_func,
    '&': functions.concat_func,
    '^': functions.exponent_func,
    '<>': functions.compare_not_eq_func,
    '>=': functions.compare_gte_func,
    '<=': functions.compare_lte_func,
    '>': functions.compare_gt_func,
    '<': functions.compare_lt_func,
    '=': functions.compare_eq_func,
}

EXCEL_FUNCTIONS = {}
EXCEL_FUNCTIONS.update(ARITHMETIC_FUNCTIONS)

EXCEL_FUNCTIONS['SUM'] = functions.sum_func
EXCEL_FUNCTIONS['SUMIFS'] = functions.sum_ifs_function
EXCEL_FUNCTIONS['MOD'] = functions.mod_func
EXCEL_FUNCTIONS['IF'] = functions.if_func
EXCEL_FUNCTIONS['IFERROR'] = functions.if_error_func
EXCEL_FUNCTIONS['MAX'] = functions.max_func
EXCEL_FUNCTIONS['MIN'] = functions.min_func
EXCEL_FUNCTIONS['LEFT'] = functions.left_func
EXCEL_FUNCTIONS['RIGHT'] = functions.right_func
EXCEL_FUNCTIONS['MID'] = functions.mid_func
EXCEL_FUNCTIONS['ISBLANK'] = functions.is_blank_func
EXCEL_FUNCTIONS['OR'] = functions.or_function
EXCEL_FUNCTIONS['AND'] = functions.and_function
EXCEL_FUNCTIONS['ROUND'] = functions.round_function
EXCEL_FUNCTIONS['ROUNDDOWN'] = functions.round_down_function
EXCEL_FUNCTIONS['FLOOR'] = functions.floor_function
EXCEL_FUNCTIONS['COUNT'] = functions.count_function
EXCEL_FUNCTIONS['COUNTIF'] = functions.countif_function
EXCEL_FUNCTIONS['COUNTBLANK'] = functions.count_blank_function
EXCEL_FUNCTIONS['ABS'] = functions.abs_function
EXCEL_FUNCTIONS['OFFSET'] = functions.offset_function
EXCEL_FUNCTIONS['MATCH'] = functions.match_function
EXCEL_FUNCTIONS['AVERAGE'] = functions.average_function
EXCEL_FUNCTIONS['AVERAGEIFS'] = functions.average_ifs_function
EXCEL_FUNCTIONS['VLOOKUP'] = functions.vlookup_function
EXCEL_FUNCTIONS['SMALL'] = functions.small_function
EXCEL_FUNCTIONS['LARGE'] = functions.large_function
EXCEL_FUNCTIONS['COUNTIFS'] = functions.count_ifs_function
EXCEL_FUNCTIONS['CONCATENATE'] = functions.concatenate


class Operation(object):
    operands_count = None
    priority = None

    def __init__(self, f_name):
        self.f_name = f_name
        self.operands_count = 1

    @property
    def f(self):
        return excel_function(EXCEL_FUNCTIONS[self.f_name])

    @property
    def is_exists(self):
        return self.f_name in EXCEL_FUNCTIONS

    def eval(self, *args):
        if self.is_exists:
            return self.f(*args)
        else:
            return FunctionNotSupported(self.f_name)


class ArithmeticOperation(Operation):
    def __init__(self, f_name, priority):
        super(ArithmeticOperation, self).__init__(f_name)
        self.operands_count = 2
        self.priority = priority


class FunctionOperation(Operation):
    def __init__(self, f_name):
        super(FunctionOperation, self).__init__(f_name)
        self.operands_count = 1
        self.priority = float('inf')
