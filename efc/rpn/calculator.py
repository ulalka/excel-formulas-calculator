# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.lexer import Lexer
from efc.rpn.parser import Parser
from efc.rpn.functions import EXCEL_FUNCTIONS
from efc.rpn.tokens import OperandToken, OperationToken, AddressToken
from efc.rpn.errors import OperandsMissing, FunctionNotSupported, UnusedOperands
import six

if six.PY2:
    range = xrange


class Calculator(object):
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def calc(self, f, ws_name, source):
        tokens_line = self.lexer.parse(f)
        rpn = self.parser.to_rpn(tokens_line)

        result = []

        result_append = result.append
        result_pop = result.pop
        for token in rpn:
            if isinstance(token, AddressToken):
                result_append(token.get_value(ws_name, source))
            elif isinstance(token, OperandToken):
                result_append(token.value)
            elif isinstance(token, OperationToken):
                try:
                    args = [result_pop() for _ in range(token.operands_count)]
                except IndexError:
                    raise OperandsMissing(token)

                try:
                    f = EXCEL_FUNCTIONS[token.src_value]
                except KeyError:
                    raise FunctionNotSupported(token.value)

                result_append(f(*reversed(args)))

        if len(result) != 1:
            raise UnusedOperands(result)
        return result[0]
