# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from efc.rpn_builder.lexer.errors import CheckSumError
from efc.utils import u


def test_check_sum_error_class():
    src_line = '1 + 2'
    parsed_line = '1+2'

    e = CheckSumError(src_line=src_line, parsed_line=parsed_line)
    template = 'Code 100. Some symbols from line are lost. Src line: {src_line}. Parsed line: {parsed_line}.'
    assert u(e) == template.format(src_line=src_line, parsed_line=parsed_line)

    with pytest.raises(CheckSumError):
        raise e
