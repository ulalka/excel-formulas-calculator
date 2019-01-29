# coding: utf8
from __future__ import unicode_literals, print_function

from efc.rpn.calculator import Calculator


def calc(formula, ws_name, source):
    return Calculator().calc(formula, ws_name, source)
