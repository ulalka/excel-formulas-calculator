# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn import tokens


def add_func(a, b):
    return a + b


def subtract_func(a, b):
    return a - b


def divide_func(a, b):
    return a / b


def multiply_func(a, b):
    return a * b


def concat_func(a, b):
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


EXCEL_FUNCTIONS = {
    tokens.AddToken: add_func,
    tokens.SubtractToken: subtract_func,
    tokens.DivideToken: divide_func,
    tokens.MultiplyToken: multiply_func,
    tokens.ConcatToken: concat_func,
    tokens.ExponentToken: exponent_func,
    tokens.CompareNotEqToken: compare_not_eq_func,
    tokens.CompareGTEToken: compare_gte_func,
    tokens.CompareLTEToken: compare_lte_func,
    tokens.CompareGTToken: compare_gt_func,
    tokens.CompareLTToken: compare_lt_func,
    tokens.CompareEqToken: compare_eq_func,
}
