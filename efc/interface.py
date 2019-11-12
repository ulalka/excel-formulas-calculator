# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def cell_to_value(self, row, column, ws_name):
        """
        :type row: int
        :type column: int
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError

    def named_range_to_cells(self, name, ws_name):
        """
        TEST_RANGE -> SingleCellOperand
        OTHER_RANGE -> CellRangeOperand
        OTHER2_RANGE -> CellSetOperand
        :type name: basestring
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError

    def max_row(self, ws_name):
        raise NotImplementedError

    def min_row(self, ws_name):
        raise NotImplementedError

    def max_column(self, ws_name):
        raise NotImplementedError

    def min_column(self, ws_name):
        raise NotImplementedError

    def has_worksheet(self, ws_name):
        raise NotImplementedError

    def has_named_range(self, name, ws_name):
        raise NotImplementedError
