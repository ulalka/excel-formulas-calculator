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
    | compare_gte
    | compare_gt
    | compare_lte
    | compare_lt
    | expression
    ;

expression
    =
    | concat
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

compare_gte::CompareGTE
    =
    left:expression '>=' ~ right:expression
    ;

compare_gt::CompareGT
    =
    left:expression '>' ~ right:expression
    ;

compare_lte::CompareLTE
    =
    left:expression '<=' ~ right:expression
    ;
 
compare_lt::CompareLT
    =
    left:expression '<' ~ right:expression
    ;

addition::Add
    =
    left:term '+' ~ right:expression
    ;

concat::Concat
    =
    left:term '&' ~ right:expression
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
    left:value '^' ~ right:value
    ;

subexpression::SubExpression
    =
    '(' ~ expr:expression ')'
    ;

number::int
    =
    /\d+/
    ;

float::float
    =
    /\d+\.\d+/
    ;

STRING
    =
    '"' @:/[^"]*/ '"'
    ;
    
value
    =
    | functions
    | float
    | number
    | CELL_ADDRESS
    | STRING
    ;
    
functions
    =
    | SUM_FUNCTION
    | MOD_FUNCTION
    | IF_FUNCTION
    | IF_ERROR_FUNCTION
    | MAX_FUNCTION
    | LEFT_FUNCTION
    | RIGHT_FUNCTION
    | ISBLANK
    ;

SUM_FUNCTION::SumFunction
    =
    'SUM(' ~ ','>{operand:stmt}+ ')'
    ;

MOD_FUNCTION::ModFunction
    =
    'MOD(' ~ left:stmt ',' right:stmt ')'
    ;
    
LEFT_FUNCTION::LeftFunction
    =
    'LEFT(' ~ expr:stmt ',' amount:stmt ')'
    ;
    
RIGHT_FUNCTION::RightFunction
    =
    'RIGHT(' ~ expr:stmt ',' amount:stmt ')'
    ;

ISBLANK::IsBlankFunction
    =
    'ISBLANK(' ~ expr:stmt ')'
    ;

IF_FUNCTION::IFFunction
    =
    'IF(' ~ expr:stmt ',' true:stmt ',' false:stmt ')'
    ;

IF_ERROR_FUNCTION::IFERRORFunction
    =
    'IFERROR(' ~ expr:stmt ',' true:stmt ')'
    ;
    
MAX_FUNCTION::MaxFunction
    =
    'MAX(' ~ ','>{operand:stmt}+ ')'
    ;
    
CELL_ADDRESS::CellAddress
    =
    | ws_name:/\w+/ '!' ~ address:RELATIVE_CELL_ADDRESS
    | "'" ws_name:/[^']+/ "'!" ~ address:RELATIVE_CELL_ADDRESS
    | address:RELATIVE_CELL_ADDRESS
    ;

RELATIVE_CELL_ADDRESS 
    =
    | CELL_RANGE
    | SINGLE_CELL
    | NAMED_RANGE
    ;
    
CELL_RANGE::CellRange
    =
    left:SINGLE_CELL ':' ~ right:SINGLE_CELL
    ;

NAMED_RANGE::NamedRange
    =
    name:/[^\W0-9]\w+/
    ;

SINGLE_CELL::SingleCell
    =
    /&?/ column_letter:CELL_COLUMN /&?/ row:CELL_ROW
    ;

CELL_COLUMN
    =
    /[A-Z]+/
    ;

CELL_ROW::int
    =
    /\d+/
    ;
"""
