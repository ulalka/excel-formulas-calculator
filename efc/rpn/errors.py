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


class EFCNameError(EFCBaseError):
    """Named range or function does not exists"""


class OperandLikeError(EFCBaseError):
    """Errors which can be like operands"""


class FunctionNotSupported(OperandLikeError):
    """Function not found among available functions"""


class EFCValueError(OperandLikeError):
    """Error getting cell value"""


class EFCLinkError(OperandLikeError):
    """Worksheet does not exists"""


class FunctionError(OperandLikeError):
    """An error occurred while evaluating function"""


class CriticalEFCError(EFCBaseError):
    """Error when formula cannot be calculated"""


class OperandsMissing(CriticalEFCError):
    """The number of operands is more than available in stack"""

    def __init__(self, token, rpn):
        self.token = token
        self.rpn = rpn


class UnusedOperands(CriticalEFCError):
    """There are more operations, than operands available"""

    def __init__(self, lost_operands):
        self.lost_operands = lost_operands