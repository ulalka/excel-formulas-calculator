# coding: utf8

from __future__ import unicode_literals
from tatsu.objectmodel import Node


class EFCBaseNode(Node):
    pass


class AddSubNode(EFCBaseNode):
    mult = None


class Add(AddSubNode):
    mult = 1


class Subtract(AddSubNode):
    mult = -1


class Multiply(EFCBaseNode):
    pass


class Divide(EFCBaseNode):
    pass


class Exponent(EFCBaseNode):
    pass


class ConcatString(EFCBaseNode):
    pass


class SubExpression(EFCBaseNode):
    pass


class CompareBase(EFCBaseNode):
    pass


class CompareEq(CompareBase):
    pass
