# coding: utf8
from __future__ import unicode_literals, print_function

import tatsu
from efc.semantics import EFCModelBuilderSemantics
from efc.walker import FormulaWalker
from efc.grammar import GRAMMAR


def get_calculator(walker=None, grammar=GRAMMAR, semantics=None):
    walker = walker or FormulaWalker()
    semantics = semantics or EFCModelBuilderSemantics()
    parser = tatsu.compile(grammar, semantics=semantics)
    return lambda formula, ws_name, source: walker.walk(parser.parse(formula), ws_name=ws_name, source=source)


def calc(formula, ws_name, source, walker=None, grammar=GRAMMAR, semantics=None):
    return get_calculator(walker=walker, grammar=grammar, semantics=semantics)(formula, ws_name, source)
