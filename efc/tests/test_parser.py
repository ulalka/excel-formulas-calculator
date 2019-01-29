# coding: utf8

from __future__ import unicode_literals, print_function
import unittest
from efc.rpn import tokens
from efc.rpn.lexer import Lexer
from efc.rpn.parser import Parser
from itertools import izip

operations_examples = (
    ('4 + 5.54 - "hello"',
     [tokens.IntToken, tokens.FloatToken, tokens.StringToken,
      tokens.SubtractToken, tokens.AddToken]),
    ('4 + 5.54 - SUM(1,2,4)',
     [tokens.IntToken, tokens.FloatToken, tokens.IntToken, tokens.IntToken,
      tokens.IntToken, tokens.FunctionToken, tokens.SubtractToken,
      tokens.AddToken]),
    ('4 + 5.54 - SUM(1,SUM(1,2))',
     [tokens.IntToken, tokens.FloatToken, tokens.IntToken, tokens.IntToken,
      tokens.IntToken, tokens.FunctionToken, tokens.FunctionToken,
      tokens.SubtractToken, tokens.AddToken]),
    ('SUM(1,2,4) * 5',
     [tokens.IntToken, tokens.IntToken, tokens.IntToken, tokens.FunctionToken,
      tokens.IntToken, tokens.MultiplyToken]),
    ('SUM(1 + 2,2,4) * 5',
     [tokens.IntToken, tokens.IntToken, tokens.AddToken, tokens.IntToken,
      tokens.IntToken, tokens.FunctionToken, tokens.IntToken, tokens.MultiplyToken]),
)


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def classes_compare(self, examples):
        for s, result_classes in examples:
            parsed_line = self.parser.to_rpn(self.lexer.parse(s))

            self.assertEqual(len(parsed_line), len(result_classes),
                             msg='Len of tokens lines not equal.')

            for c, token in izip(result_classes, parsed_line):
                self.assertIsInstance(token, c)

    def test_operations(self):
        self.classes_compare(operations_examples)
