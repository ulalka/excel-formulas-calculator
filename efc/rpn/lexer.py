# coding: utf8

from __future__ import unicode_literals, print_function

from efc.rpn import tokens
import re

TOKENS_PRIORITY = (tokens.FloatToken, tokens.IntToken, tokens.StringToken,
                   tokens.CellRangeToken, tokens.CellAddressToken,
                   tokens.SheetNameToken, tokens.FunctionToken,
                   tokens.NameToken, tokens.ArithmeticToken,
                   tokens.CompareToken, tokens.LeftBracketToken,
                   tokens.RightBracketToken, tokens.SpaceToken)


class Lexer(object):
    def __init__(self, token_classes=TOKENS_PRIORITY):
        self.regexp, self.name_to_class = self._prepare_regexp(token_classes)

    def _prepare_regexp(self, token_classes):
        regexp_list, name_to_class = [], {}
        for c in token_classes:
            token_name = c.get_token_name()
            regexp_list.append(r'(?P<%s>%s)' % (token_name, c.pattern))
            name_to_class[token_name] = c
        return r'|'.join(regexp_list), name_to_class

    def _get_cls(self, keys):
        for key in (k for k in keys if k in self.name_to_class):
            return self.name_to_class[key]

    def parse(self, line):
        tokens_line = []
        for match in re.finditer(self.regexp, line, flags=re.UNICODE):
            cls = self.name_to_class[match.lastgroup]
            if cls != tokens.SpaceToken:
                tokens_line.append(cls(match))
        return tokens_line
