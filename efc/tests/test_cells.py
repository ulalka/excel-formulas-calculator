# coding: utf8

from __future__ import unicode_literals, print_function
import unittest

from efc import get_calculator
from efc.tests.mock import ExcelMock
from efc.errors import WorksheetDoesNotExists


class TestFormulaCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = get_calculator()
        self.source = ExcelMock()

    def test_cell_address(self):
        self.assertEqual(self.calc('A3', 'Sheet 1', self.source), 4)
        self.assertEqual(self.calc('C1', 'Sheet 1', self.source), 18)

        self.assertEqual(self.calc('B100', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('AA104', 'Yet another sheet', self.source), 45)

        with self.assertRaises(WorksheetDoesNotExists):
            self.assertEqual(self.calc('F104', 'Some error ws', self.source), 2)

        self.assertEqual(self.calc('Sheet4!A3', 'Yet another sheet', self.source), 4)
        self.assertEqual(self.calc('\'Sheet 1\'!C1', 'Yet another sheet', self.source), 18)

        # test arith with address
        self.assertEqual(self.calc('A3 + 3', 'Sheet 1', self.source), 7)
        self.assertEqual(self.calc('C1 / 9', 'Sheet 1', self.source), 2)

        self.assertEqual(self.calc('Sheet4!A3 ^ 2', 'Yet another sheet', self.source), 16)
        self.assertEqual(self.calc('\'Sheet 1\'!C1 - 4 - 1', 'Yet another sheet', self.source), 13)
