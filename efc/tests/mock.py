# coding: utf8

from __future__ import unicode_literals, print_function
from efc.interface import BaseExcelInterface
from efc.rpn.errors import EFCLinkError, EFCNameError

try:
    range = xrange
except NameError:
    # Python 3
    pass


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
    }

    named_ranges = {
        'test': [1, 2, 3, 4, 5],
        'test2': [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
    }

    def cell_to_value(self, row, column, ws_name):
        if ws_name not in self.data:
            raise EFCLinkError(ws_name)

        return self.data[ws_name].get(row, {}).get(column)

    def range_to_values(self, start_row, start_column, end_row, end_column, ws_name):
        if ws_name not in self.data:
            raise EFCLinkError(ws_name)

        result = []
        for row in range(start_row, end_row + 1):
            row_data = self.data[ws_name].get(row, {})
            result.append([row_data.get(col) for col in range(start_column, end_column + 1)])
        return result

    def named_range_to_values(self, range_name, ws_name):
        if ws_name not in self.data:
            raise EFCLinkError(ws_name)

        if range_name not in self.named_ranges:
            raise EFCNameError(ws_name)

        return self.named_ranges[range_name]
