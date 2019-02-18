# coding: utf8

from __future__ import unicode_literals, print_function
from efc.base.errors import BaseEFCException


class RPNError(BaseEFCException):
    pass


class OperandsMissing(RPNError):
    code = 300
    msg = 'The number of operands is more than available in stack for function "{f_name}"'

    def __init__(self, f_name, formula):
        self.f_name = f_name
        self.formula = formula
