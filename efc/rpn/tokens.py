# coding: utf8

from __future__ import unicode_literals, print_function
from efc.utils import col_str_to_index


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


class BoolToken(OperandToken):
    pattern = r'(TRUE|FALSE)'

    def to_python(self, m):
        return super(BoolToken, self).to_python(m) == 'TRUE'


class StringToken(OperandToken):
    pattern = r'"[^"]*"'

    def to_python(self, m):
        return super(StringToken, self).to_python(m)[1:-1]


class AddressToken(OperandToken):
    ws_name = None

    def get_value(self, ws_name, source):
        raise NotImplementedError

    @staticmethod
    def clean_ws_name(v):
        if v and v.startswith('\''):
            return v[1:-1]
        return v


class SingleCellToken(AddressToken):
    pattern = (r"((?P<single_ws_name>('[^']+')|(\w+))!)?"
               r"\$?(?P<column>[A-Z]+)\$?(?P<row>[0-9]+)")
    row, column = None, None

    def to_python(self, m):
        v = (self.ws_name,
             self.row, self.column) = (self.clean_ws_name(m['single_ws_name']),
                                       int(m['row']),
                                       col_str_to_index(m['column']))
        return v

    def get_value(self, ws_name, source):
        ws_name = self.ws_name or ws_name
        return source.cell_to_value(self.row, self.column,
                                    ws_name)


class CellsRangeToken(AddressToken):
    pattern = (r"((?P<range_ws_name>('[^']+')|(\w+))!)?"
               r"\$?(?P<column1>[A-Z]+)\$?(?P<row1>[0-9]+)"
               r":\$?(?P<column2>[A-Z]+)\$?(?P<row2>[0-9]+)")
    row1, column1 = None, None
    row2, column2 = None, None

    def to_python(self, m):
        v = (self.ws_name,
             self.row1, self.column1,
             self.row2, self.column2) = (self.clean_ws_name(m['range_ws_name']),
                                         int(m['row1']),
                                         col_str_to_index(m['column1']),
                                         int(m['row2']),
                                         col_str_to_index(m['column2']))
        return v

    def get_value(self, ws_name, source):
        ws_name = self.ws_name or ws_name
        return source.range_to_values(self.row1, self.column1,
                                      self.row2, self.column2,
                                      ws_name)


class NamedRangeToken(AddressToken):
    pattern = (r"((?P<named_range_ws_name>('[^']+')|(\w+))!)?"
               r"(?P<range_name>\w+)")
    range_name = None

    def to_python(self, m):
        v = (self.ws_name,
             self.range_name) = (self.clean_ws_name(m['named_range_ws_name']),
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


class ArithmeticToken(OperationToken):
    pass


class AddToken(ArithmeticToken):
    pattern = r'\+'


class SubtractToken(ArithmeticToken):
    pattern = r'\-'


class DivideToken(ArithmeticToken):
    pattern = r'/'


class MultiplyToken(ArithmeticToken):
    pattern = r'\*'


class ConcatToken(ArithmeticToken):
    pattern = r'\&'


class ExponentToken(ArithmeticToken):
    pattern = r'\^'


class CompareNotEqToken(ArithmeticToken):
    pattern = r'\<\>'


class CompareGTEToken(ArithmeticToken):
    pattern = r'\>\='


class CompareLTEToken(ArithmeticToken):
    pattern = r'\<\='


class CompareGTToken(ArithmeticToken):
    pattern = r'\>'


class CompareLTToken(ArithmeticToken):
    pattern = r'\<'


class CompareEqToken(ArithmeticToken):
    pattern = r'\='


class LeftBracketToken(Token):
    pattern = r'\('


class RightBracketToken(Token):
    pattern = r'\)'


class SpaceToken(Token):
    pattern = r'[ ]+'


class Separator(Token):
    pattern = r','
