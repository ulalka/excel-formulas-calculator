# coding: utf8

from __future__ import unicode_literals, print_function
from string import ascii_uppercase
import six
from efc.rpn.errors import OperandLikeError


__all__ = ('col_str_to_index', 'col_index_to_str', 'u', 'cached_property', 'digit', 'digit_or_string')


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
    base = len(ascii_uppercase)
    return sum((ascii_uppercase.index(s) + 1) * base ** (str_len - i)
               for i, s in enumerate(col_str, 1))


def col_index_to_str(i):
    base = len(ascii_uppercase)
    chars = []
    while i:
        i, r = divmod(i, base)
        if r == 0:
            r = base
            i -= 1
        chars.append(ascii_uppercase[r - 1])
    chars.reverse()
    return ''.join(chars)


def u(value):
    if isinstance(value, six.binary_type):
        return value.decode('utf8')
    elif isinstance(value, six.text_type):
        return value
    else:
        return six.u(value)


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


def digit(v):
    if isinstance(v, six.string_types):
        v = float(v)
    elif isinstance(v, bool):
        v = int(v)
    elif v is None:
        v = 0
    return v


def digit_or_string(*args):
    for arg in args:
        if isinstance(arg, OperandLikeError):
            raise arg
        else:
            try:
                arg = digit(arg)
            except ValueError:
                arg = u(arg)
        yield arg
