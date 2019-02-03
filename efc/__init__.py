# coding: utf8
from __future__ import unicode_literals, print_function

from efc.rpn.lexer import Lexer
from efc.rpn.parser import Parser
from efc.rpn.calculator import Calculator

__author__ = "Gleb Orlov <orlovgb@mail.ru>"
__version__ = "0.1.0"


def calc(formula, ws_name, source):
    return Calculator().calc(formula, ws_name, source)


def get_calculator():
    lexer = Lexer()
    parser = Parser()
    calculator = Calculator()

    def calculate(formula, ws_name, source):
        tokens_line = lexer.parse(formula)
        rpn = parser.to_rpn(tokens_line)
        return calculator.calc(rpn, ws_name, source)

    return calculate
