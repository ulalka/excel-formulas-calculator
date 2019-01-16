# coding: utf8
from __future__ import unicode_literals, print_function


class BaseFormulaException(Exception):
    pass


class WorksheetDoesNotExists(BaseFormulaException):
    """Use this exception class in excel interface, when ws does not exists."""
