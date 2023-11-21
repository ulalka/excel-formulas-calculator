# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain

from efc import Lexer, Parser
from efc.interfaces.base import BaseExcelInterface, CellInfo
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
        'Sheet6': {
            1: {1: 0, 2: 12},
            2: {1: 1, 2: 0},
            3: {1: None, 2: 'keklol'},
            4: {1: '', 2: '0'},
            5: {1: 15, 2: -1},
        },
        'TestVLookup': {
            1: {1: 13, 2: 16, 3: 18},
            2: {1: 13, 2: 17, 3: 18},
            3: {1: 4, 2: 2, 3: 8},
        },
        'TestHLookup': {
            1: {1: 13, 2: 13, 3: 4},
            2: {1: 16, 2: 17, 3: 2},
            3: {1: 18, 2: 18, 3: 8},
        },
        'TestUnique': {
            1: {1: 'A', 2: 'B', 3: 'B', 4: 'B'},
            2: {1: 1, 2: 1, 3: 6, 4: 6},
            3: {1: 2, 2: 2, 3: 7, 4: 7},
            4: {1: 3, 2: 3, 3: 8, 4: 8},
            5: {1: None, 2: None, 3: 9, 4: 9},
            6: {1: 5, 2: 5, 3: 10, 4: 10},
            7: {1: 7, 2: 7, 3: 6, 4: 6},
            8: {1: 7, 2: 7, 3: 6, 4: 6},
            9: {1: "7", 2: 7, 3: 6, 4: 6},
            10: {1: 0, 2: 0, 3: 9, 4: 9},
        },
    }

    def _get_cell_info(self, address):
        return CellInfo(self.data[address.ws_name].get(address.row, {}).get(address.column))

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
