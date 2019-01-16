# coding: utf8

from __future__ import unicode_literals, print_function


class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def named_range_to_values(self, range_name, ws_name):
        """
        :type range_name: basestring
        :type ws_name: basestring
        :rtype: (list|tuple)
        """
        raise NotImplementedError

    def range_to_values(self, start_row, start_column, end_row, end_column, ws_name):
        """
        :type start_row: int
        :type start_column: int
        :type end_row: int
        :type end_column: int
        :type ws_name: basestring
        :rtype: (list|tuple)
        """
        raise NotImplementedError

    def cell_to_value(self, row, column, ws_name):
        """
        :type row: int
        :type column: int
        :type ws_name: basestring
        :rtype: (list|tuple)
        """
        raise NotImplementedError
