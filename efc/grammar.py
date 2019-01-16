# coding: utf8

from __future__ import unicode_literals, print_function

GRAMMAR = """
start
    =
    stmt $
    ;

stmt
    =
    | compare_eq
    | compare_not_eq
    | compare_gt
    | compare_lt
    | expression
    ;

expression
    =
    | addition
    | subtraction
    | term
    ;

compare_eq::CompareEq
    =
    left:expression '=' ~ right:expression
    ;
    
compare_not_eq::CompareNotEq
    =
    left:expression '<>' ~ right:expression
    ;
    
compare_gt::CompareGT
    =
    left:expression '>' ~ right:expression
    ;
    
compare_lt::CompareLT
    =
    left:expression '<' ~ right:expression
    ;

addition::Add
    =
    left:term '+' ~ right:expression
    ;

subtraction::Subtract
    =
    left:term '-' ~ right:expression
    ;

term
    =
    | multiplication
    | division
    | factor
    ;

multiplication::Multiply
    =
    left:factor '*' ~ right:term
    ;

division::Divide
    =
    left:factor '/' ~ right:term
    ;

factor
    =
    | subexpression
    | exponent
    | value
    ;
    
exponent::Exponent
    =
    left:value '^' right:value
    ;

subexpression::SubExpression
    =
    '(' ~ expr:expression ')'
    ;

number::int
    =
    /\d+/
    ;

value
    =
    | number
    | cell_address
    ;
    
cell_address
    =
    | CELL_RANGE
    | SINGLE_CELL
    ;
    
CELL_RANGE::CellRange
    =
    | ws_name:WS_NAME '!' SINGLE_CELL ':' ~ SINGLE_CELL
    | SINGLE_CELL ':' ~ SINGLE_CELL
    ;

NAMED_RANGE::NamedRange
    =
    | ws_name:WS_NAME '!' RANGE_NAME
    | RANGE_NAME
    ;

RANGE_NAME
    =
    /[^\W0-9]\w+/
    ;

SINGLE_CELL::SingleCell
    =
    | ws_name:WS_NAME '!' /&?/ column:CELL_COLUMN /&?/ row:CELL_ROW
    | /&?/ column:CELL_COLUMN /&?/ row:CELL_ROW
    ;

CELL_COLUMN
    =
    /[A-Z]+/
    ;

CELL_ROW::int
    =
    /\d+/
    ;
    
WS_NAME
    =
    /'?.+'?/
    ;
"""
