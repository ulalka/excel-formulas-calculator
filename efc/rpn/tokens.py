# coding: utf8

from __future__ import unicode_literals, print_function
from efc.utils import col_str_to_index


class Token(object):
    pattern = None

    def __init__(self, match):
        self.src_value = match.group(0)
        self.token_value = self.get_value(match.groupdict())

    @classmethod
    def get_group_pattern(cls):
        return r'(?P<%s>%s)' % (cls.__name__, cls.pattern)

    def get_value(self, m):
        return m[self.__class__.__name__]

    def __str__(self):
        return '<%s, %s>' % (self.__class__.__name__, self.token_value)

    def __repr__(self):
        return str(self)


class OperandToken(Token):
    pass


class FloatToken(OperandToken):
    pattern = r'\d+\.\d+'

    def get_value(self, m):
        return float(super(FloatToken, self).get_value(m))


class IntToken(OperandToken):
    pattern = r'\d+'

    def get_value(self, m):
        return int(super(IntToken, self).get_value(m))


class BoolToken(OperandToken):
    pattern = r'(TRUE|FALSE)'

    def get_value(self, m):
        return super(BoolToken, self).get_value(m) == 'TRUE'


class StringToken(OperandToken):
    pattern = r'"[^"]*"'

    def get_value(self, m):
        return super(StringToken, self).get_value(m)[1:-1]


class AddressToken(OperandToken):
    @staticmethod
    def clean_ws_name(v):
        if v and v.startswith('\''):
            return v[1:-1]
        return v

    def __getattr__(self, item):
        return self.token_value[item]


class SingleCellToken(AddressToken):
    pattern = (r"((\[(?P<s_doc>\w+)\])?(?P<single_ws_name>('[^']+')|(\w+))?!)?"
               r"\$?(?P<column>[A-Z]+)\$?(?P<row>[0-9]+)(?=\b)")

    def get_value(self, m):
        return {
            'ws_name': self.clean_ws_name(m['single_ws_name']),
            'row': int(m['row']),
            'column': col_str_to_index(m['column'])
        }


class CellsRangeToken(AddressToken):
    pattern = (r"((\[(?P<r_doc>\w+)\])?(?P<range_ws_name>('[^']+')|(\w+))?!)?"
               r"\$?(?P<column1>[A-Z]+)\$?(?P<row1>[0-9]+)"
               r":\$?(?P<column2>[A-Z]+)\$?(?P<row2>[0-9]+)(?=\b)")

    def get_value(self, m):
        return {
            'ws_name': self.clean_ws_name(m['range_ws_name']),
            'row1': int(m['row1']),
            'column1': col_str_to_index(m['column1']),
            'row2': int(m['row2']),
            'column2': col_str_to_index(m['column2'])
        }


class NamedRangeToken(AddressToken):
    pattern = (r"((\[(?P<n_doc>\w+)\])?(?P<named_range_ws_name>('[^']+')|(\w+))?!)?"
               r"(?P<range_name>\w+)")

    def get_value(self, m):
        return {
            'ws_name': self.clean_ws_name(m['named_range_ws_name']),
            'name': m['range_name']
        }


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
