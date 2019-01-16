# coding: utf8

from __future__ import unicode_literals, print_function
from efc.interface import BaseExcelInterface
from efc.errors import WorksheetDoesNotExists


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
            3: {1: 4, 2: 2, 3: 8},
        },
    }

    def cell_to_value(self, row, column, ws_name):
        if ws_name not in self.data:
            raise WorksheetDoesNotExists(ws_name)
        return self.data[ws_name].get(row, {}).get(column)
