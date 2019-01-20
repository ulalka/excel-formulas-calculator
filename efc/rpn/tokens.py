# coding: utf8

from __future__ import unicode_literals, print_function


class Token(object):
    pattern = None

    def __init__(self, match):
        self.src_value = match.group(0)
        self.value = self.to_python(match.groupdict())

    @classmethod
    def get_token_name(cls):
        return cls.__name__

    def to_python(self, m):
        return m[self.get_token_name()]


class FloatToken(Token):
    pattern = r'\d+\.\d+'

    def to_python(self, m):
        return float(super(FloatToken, self).to_python(m))


class IntToken(Token):
    pattern = r'\d+'

    def to_python(self, m):
        return int(super(IntToken, self).to_python(m))


class StringToken(Token):
    pattern = r'"[^"]*"'

    def to_python(self, m):
        return super(StringToken, self).to_python(m)[1:-1]


class FunctionToken(Token):
    pattern = r'[A-Z]+(?=\()'


class NameToken(Token):
    pattern = r'\w+'


class CellRangeToken(Token):
    pattern = r'\$?(?P<row1>[A-Z]+)\$?(?P<cell1>[0-9]+):' \
              r'\$?(?P<row2>[A-Z]+)\$?(?P<cell2>[0-9]+)'

    def to_python(self, m):
        return (m['row1'], int(m['cell1'])), (m['row2'], int(m['cell2']))


class CellAddressToken(Token):
    pattern = r'\$?(?P<row>[A-Z]+)\$?(?P<cell>[0-9]+)'

    def to_python(self, m):
        return m['row'], int(m['cell'])


class SheetNameToken(Token):
    pattern = r"(?P<ws_name>('[^']+')|(\w+))!"

    def to_python(self, m):
        v = m['ws_name']
        if v.startswith("'"):
            v = v[1:-1]
        return v


class ArithmeticToken(Token):
    pattern = r'\+|-|/|\*|&|\^'


class CompareToken(Token):
    pattern = r'\<\>|\>\=|\<\=|\>|\<|\='


class BracketToken(Token):
    pass


class LeftBracketToken(BracketToken):
    pattern = r'\('


class RightBracketToken(BracketToken):
    pattern = r'\)'


class SpaceToken(Token):
    pattern = r'[ ]+'


class Separator(Token):
    pattern = r','
