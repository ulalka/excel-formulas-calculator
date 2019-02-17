# coding: utf8

from __future__ import unicode_literals, print_function
import unittest
from efc.rpn_builder.lexer import Lexer
from efc.rpn_builder.parser import operations, operands
from efc.rpn_builder.parser import Parser
from six.moves import zip

operations_examples = (
    ('4 + 5.54 - "hello"',
     [operands.SimpleOperand, operands.SimpleOperand, operands.SimpleOperand,
      operations.ArithmeticOperation, operations.ArithmeticOperation]),
    ('4 + 5.54 - SUM(1,2,4)',
     [operands.SimpleOperand, operands.SimpleOperand, operands.SimpleOperand, operands.SimpleOperand,
      operands.SimpleOperand, operations.FunctionOperation, operations.ArithmeticOperation,
      operations.ArithmeticOperation]),
    ('4 + 5.54 - SUM(1,SUM(1,2))',
     [operands.SimpleOperand, operands.SimpleOperand, operands.SimpleOperand, operands.RPNOperand,
      operations.FunctionOperation, operations.ArithmeticOperation, operations.ArithmeticOperation]),
    ('SUM(1,2,4) * 5',
     [operands.SimpleOperand, operands.SimpleOperand, operands.SimpleOperand, operations.FunctionOperation,
      operands.SimpleOperand, operations.ArithmeticOperation]),
    ('SUM(1 + 2,2,4) * 5',
     [operands.RPNOperand, operands.SimpleOperand,
      operands.SimpleOperand, operations.FunctionOperation, operands.SimpleOperand, operations.ArithmeticOperation]),
)


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def classes_compare(self, examples):
        for s, result_classes in examples:
            parsed_line = self.parser.to_rpn(self.lexer.parse(s), None, None)

            self.assertEqual(len(parsed_line), len(result_classes),
                             msg='Len of tokens lines not equal.')

            for c, token in zip(result_classes, parsed_line):
                self.assertIsInstance(token, c)

    def test_operations(self):
        self.classes_compare(operations_examples)
