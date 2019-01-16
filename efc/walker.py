# coding: utf8

from __future__ import unicode_literals, print_function

from tatsu.walkers import NodeWalker
from efc.nodes import AddSubNode


class FormulaWalker(NodeWalker):
    """
    Class for calculating formula value
    """

    def walk_object(self, node, *args, **kwargs):
        return node

    def walk__add(self, node, *args, **kwargs):
        return self.walk(node.left) + self.walk(node.right)

    def walk__subtract(self, node, *args, **kwargs):
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

    def walk__multiply(self, node, *args, **kwargs):
        return self.walk(node.left) * self.walk(node.right)

    def walk__divide(self, node, *args, **kwargs):
        return self.walk(node.left) / self.walk(node.right)

    def walk__exponent(self, node, *args, **kwargs):
        return self.walk(node.left) ** self.walk(node.right)

    def walk__compare_eq(self, node, *args, **kwargs):
        return self.walk(node.left) == self.walk(node.right)

    def walk__compare_not_eq(self, node, *args, **kwargs):
        return self.walk(node.left) != self.walk(node.right)

    def walk__compare_gt(self, node, *args, **kwargs):
        return self.walk(node.left) > self.walk(node.right)

    def walk__compare_gte(self, node, *args, **kwargs):
        return self.walk(node.left) >= self.walk(node.right)

    def walk__compare_lt(self, node, *args, **kwargs):
        return self.walk(node.left) < self.walk(node.right)

    def walk__compare_lte(self, node, *args, **kwargs):
        return self.walk(node.left) <= self.walk(node.right)

    def walk__sub_expression(self, node, *args, **kwargs):
        return self.walk(node.expr)
