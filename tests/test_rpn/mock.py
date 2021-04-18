# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain

from efc import Lexer, Parser
from efc.interfaces.base import BaseExcelInterface
from efc.rpn_builder.parser.operands import CellSetOperand, SingleCellOperand


class ExcelMock(BaseExcelInterface):
    data = {
        'Sheet 1': {
            1: {1: 13, 2: 16, 3: 18},
            3: {1: 4, 2: 2, 3: 8},
        },
        'Yet another sheet': {
            100: {1: 4, 2: 2, 3: 8},
            104: {1: 4, 2: 2, 3: 8, 27: 45},
        },
        'Sheet4': {
            1: {1: 13, 2: 16, 3: 18},
            2: {1: 13, 2: 16, 3: 18},
            3: {1: 4, 2: 2, 3: 8},
        },
        'Sheet5': {
            1: {1: '', 2: 16, 3: None},
            2: {1: 13, 2: '', 3: 18},
            3: {1: None, 2: 2, 3: ''},
        },
    }

    def _cell_to_value(self, row, column, ws_name):
        return self.data[ws_name].get(row, {}).get(column)

    @property
    def named_ranges(self):
        op_set = CellSetOperand(ws_name='Sheet 1', source=self)
        op_set.add_row([SingleCellOperand(1, 2, ws_name='Sheet 1', source=self),
                        SingleCellOperand(1, 3, ws_name='Sheet 1', source=self)])
        return {
            'test': SingleCellOperand(1, 2, ws_name='Sheet 1', source=self),
            'test2': op_set
        }

    def _get_named_range_formula(self, name, ws_name):
        pass

    def _named_range_to_cells(self, name, ws_name):
        return self.named_ranges[name]

    def _has_worksheet(self, ws_name):
        return ws_name in self.data

    def _has_named_range(self, name, ws_name):
        return name in self.named_ranges

    def _min_row(self, ws_name):
        return min(self.data[ws_name])

    def _min_column(self, ws_name):
        return min(chain(*self.data[ws_name].values()))

    def _max_row(self, ws_name):
        return max(self.data[ws_name])

    def _max_column(self, ws_name):
        return max(chain(*self.data[ws_name].values()))


def get_calculator():
    lexer = Lexer()
    parser = Parser()

    def calculate(formula, ws_name, source):
        tokens_line = lexer.parse(formula)
        rpn = parser.to_rpn(tokens_line, ws_name, source)
        return rpn.calc(ws_name, source)

    return calculate
