# coding: utf8

from __future__ import unicode_literals, print_function

from tatsu.walkers import NodeWalker
from efc.nodes import AddSubNode, SingleCell, CellRange


class FormulaWalker(NodeWalker):
    """
    Class for calculating formula value
    """

    def walk_object(self, node, **context):
        return node

    def walk__add(self, node, **context):
        return self.walk(node.left, **context) + self.walk(node.right, **context)

    def walk__subtract(self, node, **context):
        if not isinstance(node.right, AddSubNode):
            return self.walk(node.left, **context) - self.walk(node.right, **context)
        else:
            # todo may be there more beautiful way?
            # ideally semantic analyzer should optimize AST for subtract
            result = self.walk(node.left, **context)
            right_node = node.right
            mult = node.mult
            while isinstance(right_node, AddSubNode):
                result = result + mult * self.walk(right_node.left, **context)
                right_node, mult = right_node.right, right_node.mult
            result = result + mult * self.walk(right_node, **context)
            return result

    def walk__multiply(self, node, **context):
        return self.walk(node.left, **context) * self.walk(node.right, **context)

    def walk__divide(self, node, **context):
        return self.walk(node.left, **context) / self.walk(node.right, **context)

    def walk__exponent(self, node, **context):
        return self.walk(node.left, **context) ** self.walk(node.right, **context)

    def walk__compare_eq(self, node, **context):
        return self.walk(node.left, **context) == self.walk(node.right, **context)

    def walk__compare_not_eq(self, node, **context):
        return self.walk(node.left, **context) != self.walk(node.right, **context)

    def walk__compare_gt(self, node, **context):
        return self.walk(node.left, **context) > self.walk(node.right, **context)

    def walk__compare_gte(self, node, **context):
        return self.walk(node.left, **context) >= self.walk(node.right, **context)

    def walk__compare_lt(self, node, **context):
        return self.walk(node.left, **context) < self.walk(node.right, **context)

    def walk__compare_lte(self, node, **context):
        return self.walk(node.left, **context) <= self.walk(node.right, **context)

    def walk__sub_expression(self, node, **context):
        return self.walk(node.expr, **context)

    def walk__cell_address(self, node, ws_name, source, **context):
        if isinstance(node.address, SingleCell):
            return source.cell_to_value(row=node.address.row, column=node.address.column,
                                        ws_name=getattr(node, 'ws_name', ws_name))
        elif isinstance(node.address, CellRange):
            return source.range_to_values(start_row=node.address.start_row, start_column=node.address.start_column,
                                          end_row=node.address.end_row, end_column=node.address.end_column,
                                          ws_name=getattr(node, 'ws_name', ws_name))
