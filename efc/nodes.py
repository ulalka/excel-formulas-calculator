# coding: utf8

from __future__ import unicode_literals
from tatsu.objectmodel import Node
from efc.utils import col_str_to_index


class EFCBaseNode(Node):
    pass


class AddSubNode(EFCBaseNode):
    mult = None


class Add(AddSubNode):
    mult = 1


class Subtract(AddSubNode):
    mult = -1


class CellAddress(EFCBaseNode):
    pass


class CellRange(CellAddress):
    @property
    def start_row(self):
        return self.left.row

    @property
    def start_column(self):
        return col_str_to_index(self.left.column_letter)

    @property
    def end_row(self):
        return self.right.row

    @property
    def end_column(self):
        return col_str_to_index(self.right.column_letter)


class NamedRange(CellAddress):
    pass


class SingleCell(CellAddress):
    @property
    def column(self):
        return col_str_to_index(self.column_letter)


class BaseFunction(EFCBaseNode):
    pass


class OperandsMixin(object):
    @property
    def operands(self):
        operands = self.operand
        if not isinstance(self.operand, list):
            operands = [operands]
        return operands


class SumFunction(BaseFunction, OperandsMixin):
    pass


class MaxFunction(BaseFunction, OperandsMixin):
    pass


class MinFunction(MaxFunction, OperandsMixin):
    pass
