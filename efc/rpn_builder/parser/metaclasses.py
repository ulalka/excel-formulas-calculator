# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from weakref import WeakKeyDictionary

from efc.utils import join_functions


class AbstractMetaOperandCache(type):
    _sources = None

    def remove_cell(cls, source, ws_name, row, column):
        raise NotImplementedError

    def _bind_source(cls, source):
        def clear_cache():
            if source in cls._sources:
                cls._sources[source].clear()

        def remove_cell(ws_name, row, column):
            if source in cls._sources:
                cls.remove_cell(source, ws_name, row, column)

        if getattr(source, 'clear_cache_bind', None) is not None:
            source.clear_cache_bind = join_functions(clear_cache, source.clear_cache_bind)
        else:
            source.clear_cache_bind = clear_cache

        if getattr(source, 'remove_cell_bind', None) is not None:
            source.remove_cell_bind = join_functions(remove_cell, source.remove_cell_bind)
        else:
            source.remove_cell_bind = remove_cell

    def _get_source_cache(cls, source):
        try:
            return cls._sources[source]
        except KeyError:
            cache = cls._sources[source] = {}
            cls._bind_source(source)
            return cache

    @staticmethod
    def get_key(*args, **kwargs):
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        source = kwargs.get('source')
        ws_name = kwargs.get('ws_name')

        if source is not None and ws_name is not None and source.use_cache:
            cache = cls._get_source_cache(source)
            key = cls.get_key(*args, **kwargs)

            try:
                return cache[key]
            except KeyError:
                value = cache[key] = super(AbstractMetaOperandCache, cls).__call__(*args, **kwargs)
                return value
        else:
            return super(AbstractMetaOperandCache, cls).__call__(*args, **kwargs)


class MetaSingleCellOperandCache(AbstractMetaOperandCache):
    _sources = WeakKeyDictionary()

    def remove_cell(cls, source, ws_name, row, column):
        cache = cls._sources[source]

        # TODO so ugly
        for row_fixed, column_fixed in ((False, False), (False, True), (True, False), (True, True)):
            key = (ws_name, row, column, row_fixed, column_fixed)
            if key in cache:
                del cache[key]

    @staticmethod
    def get_key(row, column, row_fixed=False, column_fixed=False, ws_name=None, source=None):
        return ws_name, row, column, row_fixed, column_fixed


class MetaCellRangeOperandCache(type):
    _sources = WeakKeyDictionary()

    def remove_cell(cls, source, ws_name, row, column):
        cache = cls._sources[source]
        # TODO so ugly
        source._remove_from_range_cache(ws_name, row, column, cache)

    @staticmethod
    def get_key(row1, column1, row2, column2, row1_fixed=False, column1_fixed=False, row2_fixed=False,
                column2_fixed=False, ws_name=None, source=None):
        return ws_name, row1, column1, row2, column2, row1_fixed, column1_fixed, row2_fixed, column2_fixed
