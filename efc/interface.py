# coding: utf8

from __future__ import unicode_literals, print_function


class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def named_range_to_values(self, range_name, ws_name):
        """
        A1:A4 -> [A1, A2, A3, A4]
        A1:D1 -> [A1, B1, C1, D1]
        A1:D2 -> [[A1, B1, C1, D1], [A2, B2, C2, D2]]
        :type range_name: basestring
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError

    def range_to_values(self, start_row, start_column, end_row, end_column, ws_name):
        """
        A1:A4 -> [A1, A2, A3, A4]
        A1:D1 -> [A1, B1, C1, D1]
        A1:D2 -> [[A1, B1, C1, D1], [A2, B2, C2, D2]]
        :type start_row: int
        :type start_column: int
        :type end_row: int
        :type end_column: int
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError

    def cell_to_value(self, row, column, ws_name):
        """
        :type row: int
        :type column: int
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError
