# coding: utf8
from __future__ import unicode_literals, print_function

import tatsu
from efc.semantics import EFCModelBuilderSemantics
from efc.walker import FormulaWalker
from efc.grammar import GRAMMAR


def get_calculator(source, walker=FormulaWalker, grammar=GRAMMAR, semantics=None):
    walker = walker(source)
    semantics = semantics or EFCModelBuilderSemantics()
    parser = tatsu.compile(grammar, semantics=semantics)
    return lambda formula: walker.walk(parser.parse(formula))


def calc(formula, source, walker=FormulaWalker, grammar=GRAMMAR, semantics=None):
    semantics = semantics or EFCModelBuilderSemantics()
    ast = tatsu.parse(grammar=grammar, semantics=semantics, input=formula)
    return walker(source).walk(ast)
