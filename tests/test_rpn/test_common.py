import logging

from efc.rpn_builder.parser.operands import ValueErrorOperand


def test_logging():
    op = ValueErrorOperand()
    try:
        op.value
    except ValueErrorOperand:
        logging.exception('Error')
