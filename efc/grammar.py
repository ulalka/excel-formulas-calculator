# coding: utf8

from __future__ import unicode_literals

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
