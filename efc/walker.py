# coding: utf8

from __future__ import unicode_literals, print_function

from tatsu.walkers import NodeWalker
from efc.nodes import AddSubNode


class FormulaWalker(NodeWalker):
    def __init__(self, source):
        """
        Class for calculating formula value
        :type source: efc.interface.BaseExcelInterface
        """
        self.source = source

    def walk_object(self, node):
        return node

    def walk__add(self, node):
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node):
        if not isinstance(node.right, AddSubNode):
            return self.walk(node.left) - self.walk(node.right)
        else:
            # todo may be there more beautiful way?
            # ideally semantic analyzer should optimize AST for subtract
            result = self.walk(node.left)
            right_node = node.right
            mult = node.mult
            while isinstance(right_node, AddSubNode):
                result = result + mult * self.walk(right_node.left)
                right_node, mult = right_node.right, right_node.mult
            result = result + mult * self.walk(right_node)
            return result

    def walk__multiply(self, node):
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node):
        return self.walk(node.left) / self.walk(node.right)

    def walk__exponent(self, node):
        return self.walk(node.left) ** self.walk(node.right)

    def walk__compare_eq(self, node):
        return self.walk(node.left) == self.walk(node.right)

    def walk__compare_not_eq(self, node):
        return self.walk(node.left) != self.walk(node.right)

    def walk__compare_gt(self, node):
        return self.walk(node.left) > self.walk(node.right)

    def walk__compare_lt(self, node):
        return self.walk(node.left) < self.walk(node.right)

    def walk__sub_expression(self, node):
        return self.walk(node.expr)
