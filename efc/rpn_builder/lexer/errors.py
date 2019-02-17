# coding: utf8

from __future__ import unicode_literals, print_function
from efc.utils import BaseEFCException


class BaseLexerError(BaseEFCException):
    pass


class CheckSumError(BaseLexerError):
    code = 100
    msg = 'Some symbols from line are lost. Src line: {src_line}. Parsed line: {parsed_line}.'

    def __init__(self, src_line, parsed_line):
        self.src_line = src_line
        self.parsed_line = parsed_line
