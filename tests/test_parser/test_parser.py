# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from six.moves import zip

from efc.rpn_builder.lexer import Lexer
from efc.rpn_builder.parser import operands, operations, Parser


@pytest.fixture(scope='module')
def parse():
    lexer = Lexer()
    parser = Parser()
    return lambda line: parser.to_rpn(lexer.parse(line), None, None)


@pytest.mark.parametrize(
    ['line', 'token_types'],
    (
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
              operands.SimpleOperand, operations.FunctionOperation, operands.SimpleOperand,
              operations.ArithmeticOperation]),
    )
)
def test_operations(parse, line, token_types):
    parsed_line = parse(line)
    assert len(parsed_line) == len(token_types), 'Len of tokens lines not equal'

    for c, token in zip(token_types, parsed_line):
        assert isinstance(token, c)
