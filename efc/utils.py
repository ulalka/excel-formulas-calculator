# coding: utf8

from __future__ import unicode_literals, print_function
from string import ascii_uppercase
import six


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


def u(value):
    if isinstance(value, six.binary_type):
        return value.decode('utf8')
    elif isinstance(value, six.text_type):
        return value
    else:
        return six.u(value)
