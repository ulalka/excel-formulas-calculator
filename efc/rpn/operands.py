# -*- coding: utf8 -*-
from __future__ import unicode_literals
from efc.utils import cached_property, digit, u
from efc.rpn.errors import OperandLikeError, EFCValueError, EFCLinkError
from collections import defaultdict

from six.moves import range


class Operand(object):
    value = None

    def __init__(self, ws_name=None, source=None):
        self.ws_name = ws_name
        self.source = source

    @property
    def digit(self):
        """Digit type"""
        return digit(self.value)

    @property
    def string(self):
        """String type"""
        return u(self.value)

    @property
    def any(self):
        """Any type: digit or string"""
        try:
            return self.digit
        except ValueError:
            return self.string

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return self.string


class ErrorOperand(OperandLikeError, Operand):
    msg = '#ERROR!'

    @property
    def value(self):
        raise self

    def __str__(self):
        return self.msg


class ValueErrorOperand(EFCValueError, ErrorOperand):
    msg = '#VALUE!'


class LinkErrorOperand(EFCLinkError, ErrorOperand):
    msg = '#REF!'


class ZeroDivisionErrorOperand(ZeroDivisionError, ErrorOperand):
    msg = '#DIV/0!'


class SimpleOperand(Operand):
    def __init__(self, value, *args, **kwargs):
        super(SimpleOperand, self).__init__(*args, **kwargs)
        self.value = value


class AddressOperand(Operand):
    @property
    def value(self):
        raise NotImplementedError


class SingleCellOperand(AddressOperand):
    def __init__(self, row, column, *args, **kwargs):
        super(SingleCellOperand, self).__init__(*args, **kwargs)
        self.row = row
        self.column = column

    @cached_property
    def value(self):
        try:
            return self.source.cell_to_value(self.row, self.column, self.ws_name)
        except EFCLinkError:
            return LinkErrorOperand()


class SetOperand(Operand):
    operands_type = None

    def __init__(self, *args, **kwargs):
        super(SetOperand, self).__init__(*args, **kwargs)
        self._items = defaultdict(list)

    def check_type(self, items):
        if isinstance(items, list):
            if any(not isinstance(i, self.operands_type) for i in items):
                raise ValueErrorOperand()
        elif not isinstance(items, self.operands_type):
            raise ValueErrorOperand()

    def add_cell(self, item, row=0):
        self.check_type(item)
        self._items[row].append(item)

    def add_many(self, items, row=0):
        self.check_type(items)
        append = self._items[row].append
        for cell in items:
            append(cell)

    def add_row(self, items):
        self.check_type(items)
        r = max(self._items) + 1 if self._items else 1
        self.add_many(items, r)

    def get_iter(self):
        for r in sorted(self._items.keys()):
            for cell in self._items[r]:
                yield cell

    def __iter__(self):
        return self.get_iter()

    @cached_property
    def value(self):
        return list(self)


class CellSetOperand(SetOperand):
    operands_type = SingleCellOperand


class SimpleSetOperand(SetOperand):
    operands_type = SimpleOperand


class CellRangeOperand(AddressOperand):
    def __init__(self, row1, column1, row2, column2, *args, **kwargs):
        super(CellRangeOperand, self).__init__(*args, **kwargs)
        self.row1 = row1
        self.column1 = column1
        self.row2 = row2
        self.column2 = column2

    @cached_property
    def value(self):
        cells_set = CellSetOperand(ws_name=self.ws_name, source=self.source)
        if self.row1 == self.row2:
            cells_set.add_row([SingleCellOperand(self.row1, c, self.ws_name, self.source)
                               for c in range(self.column1, self.column2 + 1)])
        elif self.column1 == self.column2:
            cells_set.add_row([SingleCellOperand(r, self.column1, self.ws_name, self.source)
                               for r in range(self.row1, self.row2 + 1)])
        else:
            for r in range(self.row1, self.row2 + 1):
                cells_set.add_row([SingleCellOperand(r, c, self.ws_name, self.source)
                                   for c in range(self.column1, self.column2 + 1)])

        return cells_set


class NamedRangeOperand(AddressOperand):
    def __init__(self, name, *args, **kwargs):
        super(NamedRangeOperand, self).__init__(*args, **kwargs)
        self.name = name

    @cached_property
    def value(self):
        return self.source.named_range_to_cells(self.name, self.ws_name)
