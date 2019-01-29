# coding: utf8

from __future__ import unicode_literals, print_function

from efc.rpn import tokens
import re
from collections import OrderedDict

TOKENS_PRIORITY = (
    tokens.FloatToken,
    tokens.IntToken,
    tokens.BoolToken,
    tokens.StringToken,
    tokens.FunctionToken,
    tokens.CellsRangeToken,
    tokens.SingleCellToken,
    tokens.NamedRangeToken,
    tokens.AddToken,
    tokens.SubtractToken,
    tokens.DivideToken,
    tokens.MultiplyToken,
    tokens.ConcatToken,
    tokens.ExponentToken,
    tokens.CompareNotEqToken,
    tokens.CompareGTEToken,
    tokens.CompareLTEToken,
    tokens.CompareGTToken,
    tokens.CompareLTToken,
    tokens.CompareEqToken,
    tokens.LeftBracketToken,
    tokens.RightBracketToken,
    tokens.SpaceToken,
    tokens.Separator,
)


class TokensLine(object):
    def __init__(self):
        self._tokens = []
        self._pointer = 0

    def next(self):
        if self._pointer >= len(self._tokens):
            return None

        v = self._tokens[self._pointer]
        self._pointer += 1
        return v

    def add(self, token):
        self._tokens.append(token)

    def __len__(self):
        return len(self._tokens)

    def __iter__(self):
        return iter(self._tokens)


class Lexer(object):
    def __init__(self):
        self.lexer_tokens = OrderedDict()
        self.regexp = None

        self.prepare_regexp()

    def prepare_regexp(self):
        regexp_list = []
        for c in TOKENS_PRIORITY:
            self.lexer_tokens[c.__name__] = c
            regexp_list.append(c.get_group_pattern())
        self.regexp = r'|'.join(regexp_list)

    def parse(self, line):
        lexer_tokens = self.lexer_tokens

        tokens_line = TokensLine()
        for match in re.finditer(self.regexp, line, flags=re.UNICODE):
            cls = lexer_tokens[match.lastgroup]
            if cls != tokens.SpaceToken:
                tokens_line.add(cls(match))
        return tokens_line
