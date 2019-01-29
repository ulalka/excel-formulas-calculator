# coding: utf8

from __future__ import unicode_literals, print_function


class BaseRPNError(Exception):
    pass


class ParserError(BaseRPNError):
    pass


class InconsistentParentheses(ParserError):
    pass


class SeparatorWithoutFunction(ParserError):
    pass


class CalculationError(BaseRPNError):
    pass


class OperandsMissing(CalculationError):
    pass


class FunctionNotSupported(CalculationError):
    pass


class UnusedOperands(CalculationError):
    pass
