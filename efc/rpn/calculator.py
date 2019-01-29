# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.lexer import Lexer
from efc.rpn.parser import Parser
from efc.rpn.functions import EXCEL_FUNCTIONS
from efc.rpn.tokens import OperandToken, OperationToken, AddressToken
from efc.rpn.errors import (OperandsMissing, UnusedOperands, FunctionNotSupported, OperandLikeError,
                            EFCValueError, CriticalEFCError)
import six

if six.PY2:
    range = xrange


class Calculator(object):
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def compute_rpn(self, rpn, ws_name, source):
        result = []

        result_append = result.append
        result_pop = result.pop
        for token in rpn:
            if isinstance(token, AddressToken):
                try:
                    v = token.get_value(ws_name, source)
                except OperandLikeError as v:
                    pass
                except:
                    v = EFCValueError()
                result_append(v)
            elif isinstance(token, OperandToken):
                result_append(token.value)
            elif isinstance(token, OperationToken):
                try:
                    args = [result_pop() for _ in range(token.operands_count)]
                except IndexError:
                    raise OperandsMissing(token, rpn)

                args.reverse()

                try:
                    f = EXCEL_FUNCTIONS[token.src_value]
                except KeyError:
                    result_append(FunctionNotSupported())
                    continue
                try:
                    v = f(*args)
                except OperandLikeError as v:
                    pass
                except CriticalEFCError:
                    raise
                except:
                    v = OperandLikeError()
                result_append(v)

        if len(result) != 1:
            raise UnusedOperands(result)
        return result[0]

    def calc(self, formula, ws_name, source):
        tokens_line = self.lexer.parse(formula)
        rpn = self.parser.to_rpn(tokens_line)
        return self.compute_rpn(rpn, ws_name, source)
