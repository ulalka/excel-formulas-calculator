# coding: utf8

from __future__ import unicode_literals, print_function
import unittest

from tests.mock import ExcelMock
from efc.rpn.operands import LinkErrorOperand
from efc import get_calculator


class TestCells(unittest.TestCase):
    def setUp(self):
        self.calc = get_calculator()
        self.source = ExcelMock()

    def test_cell_address(self):
        self.assertEqual(self.calc('A3', 'Sheet 1', self.source).value, 4)
        self.assertEqual(self.calc('C1', 'Sheet 1', self.source).value, 18)

        self.assertEqual(self.calc('B100', 'Yet another sheet', self.source).value, 2)
        self.assertEqual(self.calc('AA104', 'Yet another sheet', self.source).value, 45)

        self.assertIsInstance(self.calc('F104', 'Some error ws', self.source).value, LinkErrorOperand)

        self.assertEqual(self.calc('Sheet4!A3', 'Yet another sheet', self.source).value, 4)
        self.assertEqual(self.calc('\'Sheet 1\'!C1', 'Yet another sheet', self.source).value, 18)

        # test arith with address
        self.assertEqual(self.calc('A3 + 3', 'Sheet 1', self.source).value, 7)
        self.assertEqual(self.calc('C1 / 9', 'Sheet 1', self.source).value, 2)

        self.assertEqual(self.calc('Sheet4!A3 ^ 2', 'Yet another sheet', self.source).value, 16)
        self.assertEqual(self.calc('\'Sheet 1\'!C1 - 4 - 1', 'Yet another sheet', self.source).value, 13)

        result = self.calc('Sheet4!A1:B3', 'Yet another sheet', self.source)
        self.assertEqual([c.value for c in result.value], [13, 16, 13, 16, 4, 2])

        self.assertEqual(self.calc('Sheet4!test', 'Yet another sheet', self.source).value, 16)
        self.assertEqual(self.calc('SUM(Sheet4!test2)', 'Yet another sheet', self.source).value, 34)
        self.assertEqual(self.calc('SUM([0]Sheet4!test2)', 'Yet another sheet', self.source).value, 34)
