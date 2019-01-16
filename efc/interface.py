# coding: utf8

from __future__ import unicode_literals, print_function


class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def named_range_to_values(self, range_name, ws_name):
        raise NotImplemented

    def range_to_values(self, start_row, start_col, end_row, end_col, ws_name):
        raise NotImplemented

    def cell_to_value(self, row, col, ws_name):
        raise NotImplemented
