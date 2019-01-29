# coding: utf8

from __future__ import unicode_literals, print_function
from string import uppercase


def col_str_to_index(col_str):
    """
    A -> 1
    B -> 2
    Z -> 26
    AA -> 27
    :param basestring col_str: [A-Z]+
    :rtype: int
    """
    str_len = len(col_str)
    base = len(uppercase)
    return sum((uppercase.index(s) + 1) * base ** (str_len - i)
               for i, s in enumerate(col_str, 1))


class Matrix(object):
    def __init__(self, m):
        self._m = m

    def iter_values(self):
        for row in self._m:
            for value in row:
                yield value

    def __iter__(self):
        return self.iter_values()


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


def to_unicode(value):
    if isinstance(value, str):
        return value.decode('utf8')
    elif isinstance(value, unicode):
        return value
    else:
        return str(value).decode('utf8')
