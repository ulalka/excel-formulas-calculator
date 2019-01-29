# coding: utf8

from __future__ import unicode_literals, print_function
import unittest
from efc.rpn import tokens
from efc.rpn.lexer import Lexer
from itertools import izip

operands_examples = (
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

operators_examples = (
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


class LexerTestCase(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def classes_compare(self, examples):
        for s, result_classes in examples:
            parsed_line = self.lexer.parse(s)

            self.assertEqual(len(parsed_line), len(result_classes),
                             msg='Len of tokens lines not equal.')

            for c, token in izip(result_classes, parsed_line):
                self.assertIsInstance(token, c)

    def test_operands(self):
        self.classes_compare(operands_examples)

    def test_operators(self):
        self.classes_compare(operators_examples)
