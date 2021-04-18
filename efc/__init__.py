# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from efc.rpn_builder.lexer import Lexer
from efc.rpn_builder.parser import Parser
from efc.rpn_builder.rpn import RPN

__author__ = 'Gleb Orlov <orlovgb@mail.ru>'
__version__ = '0.1.33'


def calc(formula, ws_name, source):
    return Parser().to_rpn(Lexer().parse(formula), ws_name, source).calc(formula, ws_name, source)


def get_calculator():
    lexer = Lexer()
    parser = Parser()

    def calculate(formula, ws_name, source):
        tokens_line = lexer.parse(formula)
        rpn = parser.to_rpn(tokens_line, ws_name, source)
        return rpn.calc(ws_name, source)

    return calculate
