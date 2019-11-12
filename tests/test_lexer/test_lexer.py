# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from six.moves import zip

from efc.rpn_builder.lexer import Lexer, tokens


@pytest.fixture(scope='module')
def lexer():
    return Lexer()


@pytest.mark.parametrize(
    ['line', 'token_types'],
    (
            ('FALSE', [tokens.BoolToken]),
            ('TRUE', [tokens.BoolToken]),
            ('4', [tokens.IntToken]),
            ('5.54', [tokens.FloatToken]),
            ('"hello"', [tokens.StringToken]),
            ('A4', [tokens.SingleCellToken]),
            ('$A$4', [tokens.SingleCellToken]),
            ('$A4', [tokens.SingleCellToken]),
            ('A$4', [tokens.SingleCellToken]),
            ('A$4:AAA5', [tokens.CellsRangeToken]),
            ('\'List\'!$A$4', [tokens.SingleCellToken]),
            ('\'List 1\'!A$4', [tokens.SingleCellToken]),
            ('\'List 1\'!A$4:AAA5', [tokens.CellsRangeToken]),
            ('\'List 1\'!hello', [tokens.NamedRangeToken]),
            ('SUM(', [tokens.FunctionToken, tokens.LeftBracketToken]),
            ('SUM', [tokens.NamedRangeToken]),
            ('SUM TRUE', [tokens.NamedRangeToken, tokens.BoolToken]),
            ('Hello Mister', [tokens.NamedRangeToken, tokens.NamedRangeToken]),
            ('SUM(34,43)',
             [tokens.FunctionToken, tokens.LeftBracketToken, tokens.IntToken,
              tokens.Separator, tokens.IntToken, tokens.RightBracketToken]),
    )
)
def test_operands_parse(lexer, line, token_types):
    parsed_line = lexer.parse(line)
    assert len(parsed_line) == len(token_types), 'Len of tokens lines not equal'

    for c, token in zip(token_types, parsed_line):
        assert isinstance(token, c)


@pytest.mark.parametrize(
    ['line', 'token_types'],
    (
            ('+', [tokens.AddToken]),
            ('-', [tokens.SubtractToken]),
            ('/', [tokens.DivideToken]),
            ('*', [tokens.MultiplyToken]),
            ('&', [tokens.ConcatToken]),
            ('^', [tokens.ExponentToken]),
            ('<>', [tokens.CompareNotEqToken]),
            ('>=', [tokens.CompareGTEToken]),
            ('<=', [tokens.CompareLTEToken]),
            ('>', [tokens.CompareGTToken]),
            ('<', [tokens.CompareLTToken]),
            ('=', [tokens.CompareEqToken]),
            ('4 + 5.54 - "hello"',
             [tokens.IntToken, tokens.AddToken, tokens.FloatToken, tokens.SubtractToken,
              tokens.StringToken]),
            ('4+5.54-"hello"+\'List 1\'!hello',
             [tokens.IntToken, tokens.AddToken, tokens.FloatToken, tokens.SubtractToken,
              tokens.StringToken, tokens.AddToken, tokens.NamedRangeToken]),
    )
)
def test_operators_parse(lexer, line, token_types):
    parsed_line = lexer.parse(line)
    assert len(parsed_line) == len(token_types), 'Len of tokens lines not equal'

    for c, token in zip(token_types, parsed_line):
        assert isinstance(token, c)
