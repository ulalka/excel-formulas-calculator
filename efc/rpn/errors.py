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


class EFCBaseError(Exception):
    def __init__(self, exc=None):
        self.exc = exc


class OperandLikeError(EFCBaseError):
    """Errors which can be like operands"""


class EFCValueError(OperandLikeError):
    """Error getting cell value"""


class EFCLinkError(OperandLikeError):
    """Worksheet does not exists"""


class CriticalEFCError(EFCBaseError):
    """Error when formula cannot be calculated"""


class ResultNotFoundError(EFCBaseError):
    """Result not found"""


class OperandsMissing(CriticalEFCError):
    """The number of operands is more than available in stack"""

    def __init__(self, token, rpn):
        self.token = token
        self.rpn = rpn


class UnusedOperands(CriticalEFCError):
    """There are more operations, than operands available"""

    def __init__(self, lost_operands):
        self.lost_operands = lost_operands
