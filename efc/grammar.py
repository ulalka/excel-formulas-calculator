# coding: utf8

from __future__ import unicode_literals

GRAMMAR = """
start
    =
    | compare_eq $
    | expression $
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
    | number
    ;

exponent::Exponent
    =
    left:number '^' right:number
    ;

subexpression::SubExpression
    =
    '(' ~ expr:expression ')'
    ;


number::int
    =
    /\d+/
    ;
"""
