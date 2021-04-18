# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from efc import Lexer, Parser
from efc.interfaces.cache import CacheManager
from efc.interfaces.errors import NamedRangeNotFound


class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def __init__(self, use_cache=False, lexer=Lexer, parser=Parser):
        self._caches = CacheManager() if use_cache else None

        self.lexer = lexer()
        self.parser = parser()

    def _build_rpn(self, formula, ws_name=None):
        tokens_line = self.lexer.parse(formula)
        return self.parser.to_rpn(tokens_line, ws_name=ws_name, source=self)

    def calc(self, formula, ws_name=None):
        """
        Calculate formula
        :type formula: str
        :type ws_name: str
        """
        rpn = self._build_rpn(formula, ws_name)
        return rpn.calc(ws_name, self)

    @property
    def caches(self):
        return self._caches

    def cell_to_value(self, row, column, ws_name):
        """
        :type row: int
        :type column: int
        :type ws_name: basestring
        :rtype: list
        """
        raise NotImplementedError

    def _get_named_range_formula(self, name, ws_name):
        """
        Should raise NamedRangeNotFound if named range not found
        :type name: basestring
        :type ws_name: basestring
        :rtype: basestring
        """
        raise NotImplementedError

    def named_range_to_cells(self, name, ws_name):
        f = self._get_named_range_formula(name, ws_name)
        return self.calc(f, ws_name)

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
        try:
            self._get_named_range_formula(name, ws_name)
        except NamedRangeNotFound:
            return False
        else:
            return True
