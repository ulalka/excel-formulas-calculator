# coding: utf8

from __future__ import unicode_literals, print_function
from efc.nodes import SingleCell, CellRange, NamedRange
from efc.utils import Matrix


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

    def get_value(self, address, ws_name):
        if isinstance(address, SingleCell):
            result = self.cell_to_value(row=address.row, column=address.column, ws_name=ws_name)
        elif isinstance(address, CellRange):
            result = self.range_to_values(start_row=address.start_row, start_column=address.start_column,
                                          end_row=address.end_row, end_column=address.end_column,
                                          ws_name=ws_name)
        elif isinstance(address, NamedRange):
            result = self.named_range_to_values(range_name=address.name,
                                                ws_name=ws_name)
        else:
            raise ValueError('Unsupported address type "%s"' % address)

        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            result = Matrix(result)
        return result
