# coding: utf8

from __future__ import unicode_literals, print_function
import unittest

from efc.rpn.calculator import Calculator
from efc.tests.mock import ExcelMock


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator().calc
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

        # IF
        self.assertEqual(self.calc('IF(2>1,1,2)', 'Yet another sheet', self.source), 1)
        self.assertEqual(self.calc('IF(\'Sheet 1\'!A3 = 4,\'Sheet 1\'!C3, 0)', 'Yet another sheet', self.source), 8)

        # IFERROR
        self.assertEqual(self.calc('IFERROR(5/0,1)', 'Yet another sheet', self.source), 1)
        self.assertEqual(self.calc('IFERROR(5+6, 0)', 'Yet another sheet', self.source), 11)

        # MAX
        self.assertEqual(self.calc('MAX(Sheet4!A1:B3)', 'Yet another sheet', self.source), 16)
        self.assertEqual(self.calc('MAX(Sheet4!A1:B3,100)', 'Yet another sheet', self.source), 100)

        # MIN
        self.assertEqual(self.calc('MIN(Sheet4!A1:B3)', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('MIN(Sheet4!A1:B3,1)', 'Yet another sheet', self.source), 1)

        # LEFT & RIGHT
        self.assertEqual(self.calc('LEFT("test", 2)', 'Yet another sheet', self.source), 'te')
        self.assertEqual(self.calc('RIGHT("test", 2)', 'Yet another sheet', self.source), 'st')

        # ISBLANK
        self.assertEqual(self.calc('ISBLANK("test")', 'Yet another sheet', self.source), False)
        self.assertEqual(self.calc('ISBLANK("")', 'Yet another sheet', self.source), False)
        self.assertEqual(self.calc('ISBLANK(Sheet4!AA1)', 'Yet another sheet', self.source), True)
