# -*- coding: utf-8 -*-
from efc.utils import join_functions
from weakref import WeakKeyDictionary


class MetaSingleCellOperandCache(type):
    _sources = WeakKeyDictionary()

    def _bind_source(cls, source):
        def clear_cache():
            if source in cls._sources:
                cls._sources[source].clear()

        def remove_cell(ws_name, row, column):
            if source in cls._sources:
                cache = cls._sources[source]

                # TODO so ugly
                for row_fixed, column_fixed in ((False, False), (False, True), (True, False), (True, True)):
                    key = (ws_name, row, column, row_fixed, column_fixed)
                    if key in cache:
                        del cache[key]

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

    def __call__(cls, row, column, row_fixed=False, column_fixed=False, ws_name=None, source=None):
        if source is not None and ws_name is not None and source.use_cache:
            cache = cls._get_source_cache(source)
            key = (ws_name, row, column, row_fixed, column_fixed)

            try:
                return cache[key]
            except KeyError:
                value = cache[key] = super(MetaSingleCellOperandCache, cls).__call__(row, column, row_fixed=row_fixed,
                                                                                     column_fixed=column_fixed,
                                                                                     ws_name=ws_name,
                                                                                     source=source)
                return value
        else:
            return super(MetaSingleCellOperandCache, cls).__call__(row, column, row_fixed=row_fixed,
                                                                   column_fixed=column_fixed, ws_name=ws_name,
                                                                   source=source)


class MetaCellRangeOperandCache(type):
    _sources = WeakKeyDictionary()

    def _bind_source(cls, source):
        def clear_cache():
            if source in cls._sources:
                cls._sources[source].clear()

        def remove_cell(ws_name, row, column):
            if source in cls._sources:
                cache = cls._sources[source]

                # TODO so ugly
                source._remove_from_range_cache(ws_name, row, column, cache)

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

    def __call__(cls, row1, column1, row2, column2,
                 row1_fixed=False, column1_fixed=False, row2_fixed=False, column2_fixed=False,
                 ws_name=None, source=None):
        if source is not None and ws_name is not None and source.use_cache:
            cache = cls._get_source_cache(source)
            key = (ws_name, row1, column1, row2, column2, row1_fixed, column1_fixed, row2_fixed, column2_fixed)

            try:
                return cache[key]
            except KeyError:
                value = cache[key] = super(MetaCellRangeOperandCache, cls).__call__(
                    row1, column1, row2, column2, row1_fixed, column1_fixed, row2_fixed, column2_fixed, ws_name, source
                )
                return value
        else:
            return super(MetaCellRangeOperandCache, cls).__call__(row1, column1, row2, column2, row1_fixed,
                                                                  column1_fixed, row2_fixed, column2_fixed, ws_name, source)
