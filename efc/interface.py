# coding: utf8

from __future__ import unicode_literals, print_function


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

    def named_range_to_cells(self, range_name, ws_name):
        """
        TEST_RANGE -> SingleCellOperand
        OTHER_RANGE -> CellRangeOperand
        OTHER2_RANGE -> CellSetOperand
        :type range_name: basestring
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError
