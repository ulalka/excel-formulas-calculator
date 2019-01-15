# coding: utf8
from __future__ import unicode_literals

import tatsu
from tatsu.walkers import NodeWalker


class FormulaCalculator(NodeWalker):
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
    
    subexpression
        =
        '(' ~ @:expression ')'
        ;
    
    
    number::int
        =
        /\d+/
        ;
    """

    def __init__(self):
        self.parser = tatsu.compile(self.GRAMMAR, asmodel=True)

    def calculate(self, formula):
        ast = self.parser.parse(formula)
        return self.walk(ast)

    def walk_object(self, node):
        return node

    def walk__add(self, node):
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node):
        return self.walk(node.left) - self.walk(node.right)

    def walk__multiply(self, node):
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node):
        return self.walk(node.left) / self.walk(node.right)

    def walk__exponent(self, node):
        return self.walk(node.left) ** self.walk(node.right)

    def walk__compare_eq(self, node):
        return self.walk(node.left) == self.walk(node.right)
