# coding: utf8

from __future__ import unicode_literals, print_function
from efc.utils import col_str_to_index, cached_property


class Token(object):
    pattern = None

    def __init__(self, match):
        self.src_value = match.group(0)
        self.value = self.to_python(match.groupdict())

    @classmethod
    def get_group_pattern(cls):
        return r'(?P<%s>%s)' % (cls.__name__, cls.pattern)

    def to_python(self, m):
        return m[self.__class__.__name__]

    def __str__(self):
        return '<%s, %s>' % (self.__class__.__name__, self.value)

    def __repr__(self):
        return str(self)


class OperandToken(Token):
    pass


class FloatToken(OperandToken):
    pattern = r'\d+\.\d+'

    def to_python(self, m):
        return float(super(FloatToken, self).to_python(m))


class IntToken(OperandToken):
    pattern = r'\d+'

    def to_python(self, m):
        return int(super(IntToken, self).to_python(m))


class StringToken(OperandToken):
    pattern = r'"[^"]*"'

    def to_python(self, m):
        return super(StringToken, self).to_python(m)[1:-1]


class AddressToken(OperandToken):
    ws_name = None

    def get_value(self, ws_name, source):
        raise NotImplementedError


class SingleCellToken(AddressToken):
    pattern = (r"((?P<single_ws_name>('[^']+')|(\w+))!)?"
               r"\$?(?P<row>[A-Z]+)\$?(?P<column>[0-9]+)")
    row, column = None, None

    def to_python(self, m):
        v = (self.ws_name, self.row, self.column) = (m['single_ws_name'],
                                                     m['row'],
                                                     int(m['column']))
        return v

    @cached_property
    def int_column(self):
        return col_str_to_index(self.column)

    def get_value(self, ws_name, source):
        ws_name = self.ws_name or ws_name
        return source.cell_to_value(self.row, self.int_column,
                                    ws_name)


class CellsRangeToken(AddressToken):
    pattern = (r"((?P<range_ws_name>('[^']+')|(\w+))!)?"
               r"\$?(?P<row1>[A-Z]+)\$?(?P<column1>[0-9]+)"
               r":\$?(?P<row2>[A-Z]+)\$?(?P<column2>[0-9]+)")
    row1, column1 = None, None
    row2, column2 = None, None

    def to_python(self, m):
        v = (self.ws_name,
             self.row1, self.column1,
             self.row2, self.column2) = (m['single_ws_name'],
                                         m['row1'], int(m['column1']),
                                         m['row2'], int(m['column2']))
        return v

    @cached_property
    def int_column1(self):
        return col_str_to_index(self.column1)

    @cached_property
    def int_column2(self):
        return col_str_to_index(self.column2)

    def get_value(self, ws_name, source):
        ws_name = self.ws_name or ws_name
        return source.range_to_values(self.row1, self.int_column1,
                                      self.row2, self.int_column2,
                                      ws_name)


class NamedRangeToken(AddressToken):
    pattern = (r"((?P<named_range_ws_name>('[^']+')|(\w+))!)?"
               r"(?P<range_name>\w+)")
    range_name = None

    def to_python(self, m):
        v = self.ws_name, self.range_name = (m['named_range_ws_name'],
                                             m['range_name'])
        return v

    def get_value(self, ws_name, source):
        ws_name = self.ws_name or ws_name
        return source.named_range_to_values(self.range_name, ws_name)


class OperationToken(Token):
    _operands_count = 2

    def __init__(self, *args, **kwargs):
        super(OperationToken, self).__init__(*args, **kwargs)

    @property
    def operands_count(self):
        return self._operands_count

    @operands_count.setter
    def operands_count(self, v):
        self._operands_count = v


class FunctionToken(OperationToken):
    pattern = r'[A-Z]+(?=\()'


class AddToken(OperationToken):
    pattern = r'\+'


class SubtractToken(OperationToken):
    pattern = r'\-'


class DivideToken(OperationToken):
    pattern = r'/'


class MultiplyToken(OperationToken):
    pattern = r'\*'


class ConcatToken(OperationToken):
    pattern = r'\&'


class ExponentToken(OperationToken):
    pattern = r'\^'


class CompareNotEqToken(OperationToken):
    pattern = r'\<\>'


class CompareGTEToken(OperationToken):
    pattern = r'\>\='


class CompareLTEToken(OperationToken):
    pattern = r'\<\='


class CompareGTToken(OperationToken):
    pattern = r'\>'


class CompareLTToken(OperationToken):
    pattern = r'\<'


class CompareEqToken(OperationToken):
    pattern = r'\='


class LeftBracketToken(Token):
    pattern = r'\('


class RightBracketToken(Token):
    pattern = r'\)'


class SpaceToken(Token):
    pattern = r'[ ]+'


class Separator(Token):
    pattern = r','
