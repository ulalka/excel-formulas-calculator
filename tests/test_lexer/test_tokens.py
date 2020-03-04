# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re

import pytest

from efc.rpn_builder.lexer import tokens
from efc.utils import col_str_to_index


@pytest.mark.parametrize(
    ['line', 'token_type'],
    (
            ('+', tokens.AddToken),
            ('-', tokens.SubtractToken),
            ('/', tokens.DivideToken),
            ('*', tokens.MultiplyToken),
            ('&', tokens.ConcatToken),
            ('^', tokens.ExponentToken),
            ('<>', tokens.CompareNotEqToken),
            ('>=', tokens.CompareGTEToken),
            ('<=', tokens.CompareLTEToken),
            ('>', tokens.CompareGTToken),
            ('<', tokens.CompareLTToken),
            ('=', tokens.CompareEqToken),
    )
)
def test_arithmetic_tokens(line, token_type):
    match = re.match('(?P<%s>%s)' % (token_type.__name__, token_type.pattern), line)
    token = token_type(match)
    assert token.src_value == line
    assert token.token_value == line


def test_function_token():
    pattern = re.compile('(?P<%s>%s)' % (tokens.FunctionToken.__name__, tokens.FunctionToken.pattern))

    token = tokens.FunctionToken(pattern.match('SUM('))
    assert token.src_value == 'SUM'
    assert token.token_value == 'SUM'

    assert pattern.match('SUM') is None


@pytest.mark.parametrize(
    ['line', 'token_type', 'result'],
    (
            ('1', tokens.IntToken, 1),
            ('1234', tokens.IntToken, 1234),
            ('1.0', tokens.FloatToken, 1.0),
            ('111.0', tokens.FloatToken, 111.0),
            ('1.001', tokens.FloatToken, 1.001),
            ('TRUE', tokens.BoolToken, True),
            ('FALSE', tokens.BoolToken, False),
            ('"FALSE"', tokens.StringToken, 'FALSE'),
            ('"hello"', tokens.StringToken, 'hello'),
            ('"HELLO"', tokens.StringToken, 'HELLO'),
    )
)
def test_simple_type_tokens(line, token_type, result):
    match = re.match('(?P<%s>%s)' % (token_type.__name__, token_type.pattern), line)
    token = token_type(match)
    assert token.src_value == line
    assert token.token_value == result


def gen_address_ws_name(doc, ws_name, quote=False):
    name_list = []
    if doc is not None:
        name_list.append('[%s]' % doc)

    if ws_name is not None:
        name_list.append('%s' % ws_name)

    if quote and name_list:
        name_list = ["'%s'" % ''.join(name_list)]

    if doc is not None or ws_name is not None:
        name_list.append('!')
    return ''.join(name_list)


def gen_cell(row, row_fixed, col, col_fixed):
    col = ('$%s' % col if col_fixed else col) if col is not None else ''
    row = ('$%s' % row if row_fixed else row) if row is not None else ''
    return col + row


@pytest.mark.parametrize('doc', [None, 'src'])
@pytest.mark.parametrize('ws_name', [None, 'word', '1_word', 'two words'])
@pytest.mark.parametrize('row', ['1', '100'])
@pytest.mark.parametrize('column', ['A', 'AA'])
@pytest.mark.parametrize('row_fixed', [True, False])
@pytest.mark.parametrize('column_fixed', [True, False])
@pytest.mark.parametrize('quote', [False, True])
def test_single_cell_token(doc, ws_name, row, column, row_fixed, column_fixed, quote):
    if ws_name and ' ' in ws_name and not quote:
        return

    address = gen_address_ws_name(doc, ws_name, quote) + gen_cell(row, row_fixed, column, column_fixed)

    match = re.match('(?P<%s>%s)' % (tokens.SingleCellToken.__name__, tokens.SingleCellToken.pattern), address)
    token = tokens.SingleCellToken(match)
    if ws_name is None:
        assert token.ws_name is None
    else:
        assert token.ws_name == ws_name.replace('\'', '')
    assert token.row == int(row)
    assert token.column == col_str_to_index(column)
    assert token.row_fixed == row_fixed
    assert token.column_fixed == column_fixed

    with pytest.raises(KeyError):
        token.s_doc == doc


@pytest.mark.parametrize('doc', [None, 'src'])
@pytest.mark.parametrize('ws_name', [None, 'word', '1_word', 'two words'])
@pytest.mark.parametrize('row1', ['1', '100'])
@pytest.mark.parametrize('column1', ['A', 'AA'])
@pytest.mark.parametrize('row1_fixed', [True, False])
@pytest.mark.parametrize('column1_fixed', [True, False])
@pytest.mark.parametrize('row2', ['1', '100'])
@pytest.mark.parametrize('column2', ['A', 'AA'])
@pytest.mark.parametrize('row2_fixed', [True, False])
@pytest.mark.parametrize('column2_fixed', [True, False])
@pytest.mark.parametrize('quote', [False, True])
def test_cells_range_token(doc, ws_name,
                           row1, column1, row1_fixed, column1_fixed,
                           row2, column2, row2_fixed, column2_fixed, quote):
    if ws_name and ' ' in ws_name and not quote:
        return

    cells_range = '%s:%s' % (gen_cell(row1, row1_fixed, column1, column1_fixed),
                             gen_cell(row2, row2_fixed, column2, column2_fixed))
    address = gen_address_ws_name(doc, ws_name, quote) + cells_range

    match = re.match('(?P<%s>%s)' % (tokens.CellsRangeToken.__name__, tokens.CellsRangeToken.pattern), address)
    token = tokens.CellsRangeToken(match)
    if ws_name is None:
        assert token.ws_name is None
    else:
        assert token.ws_name == ws_name.replace('\'', '')
    assert token.row1 == int(row1)
    assert token.column1 == col_str_to_index(column1)
    assert token.row1_fixed == row1_fixed
    assert token.column1_fixed == column1_fixed

    assert token.row2 == int(row2)
    assert token.column2 == col_str_to_index(column2)
    assert token.row2_fixed == row2_fixed
    assert token.column2_fixed == column2_fixed

    with pytest.raises(KeyError):
        token.s_doc == doc


@pytest.mark.parametrize('doc', [None, 'src'])
@pytest.mark.parametrize('ws_name', [None, 'word', '1_word', 'two words'])
@pytest.mark.parametrize('range_name', ['name', '1_name'])
@pytest.mark.parametrize('quote', [False, True])
def test_named_range_token(doc, ws_name, range_name, quote):
    if ws_name and ' ' in ws_name and not quote:
        return

    address = gen_address_ws_name(doc, ws_name, quote) + range_name

    match = re.match('(?P<%s>%s)' % (tokens.NamedRangeToken.__name__, tokens.NamedRangeToken.pattern), address)
    token = tokens.NamedRangeToken(match)
    if ws_name is None:
        assert token.ws_name is None
    else:
        assert token.ws_name == ws_name.replace('\'', '')
    assert token.name == range_name

    with pytest.raises(KeyError):
        token.s_doc == doc
