# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractmethod
from functools import partial

from six import add_metaclass

from efc import Lexer, Parser
from efc.interfaces.cache import CacheManager
from efc.interfaces.errors import NamedRangeNotFound
from efc.rpn_builder.parser.operands import CellAddress, RPNOperand, SingleCellOperand


class CellInfo:
    def __init__(self, value, formula=None):
        self.value = value
        self.formula = formula


@add_metaclass(ABCMeta)
class BaseExcelInterface(object):
    """
    Base class to working with excel document
    """

    def __init__(self, use_cache=False, lexer=Lexer, parser=Parser):
        self._cache_manager = CacheManager() if use_cache else None

        self.lexer = lexer()
        self.parser = parser()

    def _build_rpn(self, formula, ws_name=None):
        tokens_line = self.lexer.parse(formula)
        return self.parser.to_rpn(tokens_line, ws_name=ws_name, source=self)

    def _calc_formula(self, formula, ws_name=None):
        """
        Calculate formula
        :type formula: str
        :type ws_name: str
        """
        rpn = self._build_rpn(formula, ws_name)
        return rpn.calc(ws_name, self)

    @property
    def _caches(self):
        return self._cache_manager

    def clear_cache(self):
        """Clear all caches"""
        self._caches.clear()

    @abstractmethod
    def _get_cell_info(self, address):
        """
        :type address: CellAddress
        :rtype: CellInfo
        """
        pass

    def _get_value_with_target_computable_cell(self, cell_addr, cell_info):
        """
        :type cell_addr: CellAddress
        :type cell_info: CellInfo
        """
        last_cell_address = cell_addr
        calc = partial(self._build_rpn(cell_info.formula, cell_addr.ws_name).calc, cell_addr.ws_name, self)
        while True:
            partial_result = calc()
            if isinstance(partial_result, SingleCellOperand):
                value, last_cell_address = self._cell_to_value(partial_result.cell_address)
                break
            elif isinstance(partial_result, RPNOperand):
                calc = partial_result.calc
            else:
                value = partial_result.value
                break
        return value, last_cell_address

    def _cell_to_value(self, cell_addr):
        """
        rtype: tuple[Any, CellAddress]
        """
        cell_info = self._get_cell_info(cell_addr)  # type: CellInfo

        if cell_info.formula is None:
            return cell_info.value, cell_addr
        else:
            if self._caches is not None:
                if cell_addr not in self._caches['cells']:
                    self._caches['cells'][cell_addr] = self._get_value_with_target_computable_cell(cell_addr, cell_info)
                value = self._caches['cells'][cell_addr]
            else:
                value = self._get_value_with_target_computable_cell(cell_addr, cell_info)
            return value

    @abstractmethod
    def _get_named_range_formula(self, name, ws_name):
        """
        Should raise NamedRangeNotFound if named range not found
        :type name: basestring
        :type ws_name: basestring
        :rtype: basestring
        """

    @abstractmethod
    def _max_row(self, ws_name):
        pass

    @abstractmethod
    def _min_row(self, ws_name):
        pass

    @abstractmethod
    def _max_column(self, ws_name):
        pass

    @abstractmethod
    def _min_column(self, ws_name):
        pass

    @abstractmethod
    def _has_worksheet(self, ws_name):
        pass

    def _named_range_to_cells(self, name, ws_name):
        f = self._get_named_range_formula(name, ws_name)
        return self._calc_formula(f, ws_name)

    def _has_named_range(self, name, ws_name):
        try:
            self._get_named_range_formula(name, ws_name)
        except NamedRangeNotFound:
            return False
        else:
            return True
