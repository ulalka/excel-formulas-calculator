# coding: utf8
from __future__ import unicode_literals, print_function


class BaseFormulaException(Exception):
    pass


class EFCValueError(BaseFormulaException):
    """Error in arithmetic"""


class EFCLinkError(BaseFormulaException):
    """Worksheet does not exists"""


class EFCNameError(BaseFormulaException):
    """Named range does not exists"""
