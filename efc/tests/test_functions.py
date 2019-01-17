# coding: utf8

from __future__ import unicode_literals, print_function
import unittest

from efc import get_calculator
from efc.tests.mock import ExcelMock


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.calc = get_calculator()
        self.source = ExcelMock()

    def test_cell_address(self):
        # SUM
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3)', 'Yet another sheet', self.source), 64)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3) + 1', 'Yet another sheet', self.source), 65)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3,A2:B3)', 'Sheet4', self.source), 99)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3,SUM(A3:B3))', 'Sheet4', self.source), 70)

        # MOD
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!B3,4)', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!C3)', 'Yet another sheet', self.source), 4)
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!B3 * 2)', 'Yet another sheet', self.source), 0)
