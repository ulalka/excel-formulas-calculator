# coding: utf8

from __future__ import unicode_literals, print_function
import unittest

from efc.tests.mock import ExcelMock
from efc import get_calculator


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.calc = get_calculator()
        self.source = ExcelMock()

    def test_SUM(self):
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3)', 'Yet another sheet', self.source), 64)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3) + 1', 'Yet another sheet', self.source), 65)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3,A2:B3)', 'Sheet4', self.source), 99)
        self.assertEqual(self.calc('SUM(Sheet4!A1:B3,SUM(A3:B3))', 'Sheet4', self.source), 70)

    def test_MOD(self):
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!B3,4)', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!C3)', 'Yet another sheet', self.source), 4)
        self.assertEqual(self.calc('MOD(\'Sheet 1\'!A3,\'Sheet 1\'!B3 * 2)', 'Yet another sheet', self.source), 0)

    def test_IF(self):
        self.assertEqual(self.calc('IF(2>1,1,2)', 'Yet another sheet', self.source), 1)
        self.assertEqual(self.calc('IF(TRUE,1,2)', 'Yet another sheet', self.source), 1)
        self.assertEqual(self.calc('IF(FALSE,1,2)', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('IF(\'Sheet 1\'!A3 = 4,\'Sheet 1\'!C3, 0)', 'Yet another sheet', self.source), 8)

    def test_IFERROR(self):
        self.assertEqual(self.calc('IFERROR(5/0,1)', 'Yet another sheet', self.source), 1)
        self.assertEqual(self.calc('IFERROR(5+6, 0)', 'Yet another sheet', self.source), 11)

    def test_MAX(self):
        self.assertEqual(self.calc('MAX(Sheet4!A1:B3)', 'Yet another sheet', self.source), 16)
        self.assertEqual(self.calc('MAX(Sheet4!A1:B3,100)', 'Yet another sheet', self.source), 100)

    def test_MIN(self):
        self.assertEqual(self.calc('MIN(Sheet4!A1:B3)', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('MIN(Sheet4!A1:B3,1)', 'Yet another sheet', self.source), 1)

    def test_LEFT(self):
        self.assertEqual(self.calc('LEFT("test", 2)', 'Yet another sheet', self.source), 'te')

    def test_RIGHT(self):
        self.assertEqual(self.calc('RIGHT("test", 2)', 'Yet another sheet', self.source), 'st')

    def test_ISBLANK(self):
        self.assertEqual(self.calc('ISBLANK("test")', 'Yet another sheet', self.source), False)
        self.assertEqual(self.calc('ISBLANK("")', 'Yet another sheet', self.source), False)
        self.assertEqual(self.calc('ISBLANK(Sheet4!AA1)', 'Yet another sheet', self.source), True)

    def test_OR(self):
        self.assertEqual(self.calc('OR(0,0,0,TRUE)', 'Yet another sheet', self.source), True)
        self.assertEqual(self.calc('OR(FALSE, 0)', 'Yet another sheet', self.source), False)
        self.assertEqual(self.calc('OR(FALSE, 0 + 2)', 'Yet another sheet', self.source), True)

    def test_ROUND(self):
        self.assertEqual(self.calc('ROUND(2.3456, 1)', 'Yet another sheet', self.source), 2.3)
        self.assertEqual(self.calc('ROUND(2, 2)', 'Yet another sheet', self.source), 2.0)
        self.assertEqual(self.calc('ROUND("2.34567", 2)', 'Yet another sheet', self.source), 2.35)

    def test_COUNT(self):
        self.assertEqual(self.calc('COUNT(1.3456, 1, "tesr")', 'Yet another sheet', self.source), 2)
        self.assertEqual(self.calc('COUNT(A1:C4)', 'Sheet 1', self.source), 6)

    def test_COUNTIF(self):
        self.assertEqual(self.calc('COUNTIF(A1:C4, ">4")', 'Sheet 1', self.source), 4)
        self.assertEqual(self.calc('COUNTIF(A1:C4, "13")', 'Sheet4', self.source), 2)
