# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from efc.interfaces.base import BaseExcelInterface
from efc.interfaces.errors import NamedRangeNotFound


class OpenpyxlInterface(BaseExcelInterface):
    def __init__(self, wb, *args, **kwargs):
        self.wb = wb
        super(OpenpyxlInterface, self).__init__(*args, **kwargs)

    def cell_to_value(self, row, column, ws_name):
        """Calculate cell value"""
        cell = self.wb[ws_name]._get_cell(row, column)

        if cell.data_type != 'f':
            return cell.value
        elif not self.caches:
            return self.calc(cell.value, ws_name).value
        else:
            cache_key = (ws_name, row, column)
            if cache_key not in self.caches['cells']:
                f = cell.value[1:]
                self.caches['cells'][cache_key] = self.calc(f, ws_name).value

            return self.caches['cells'][cache_key]

    def _get_named_range_formula(self, name, ws_name):
        local_sheet_id = None
        if ws_name is not None:
            local_sheet_id = self.wb.sheetnames.index(ws_name)

        for named_range in self.wb.defined_names:
            if named_range.name == name:
                if named_range.localSheetId == local_sheet_id:
                    return named_range.attr_text
        else:
            raise NamedRangeNotFound

    def max_row(self, ws_name):
        return self.wb[ws_name].max_row

    def min_row(self, ws_name):
        return self.wb[ws_name].min_row

    def max_column(self, ws_name):
        return self.wb[ws_name].max_column

    def min_column(self, ws_name):
        return self.wb[ws_name].min_column

    def has_worksheet(self, ws_name):
        return ws_name in self.wb.sheetnames
