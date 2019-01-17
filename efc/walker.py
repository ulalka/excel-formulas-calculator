# coding: utf8

from __future__ import unicode_literals, print_function

from tatsu.walkers import NodeWalker
from efc.nodes import AddSubNode
from efc.utils import Matrix
from efc.errors import EFCValueError


class FormulaWalker(NodeWalker):
    """
    Class for calculating formula value
    """

    def walk_object(self, node, **context):
        return node

    def walk__add(self, node, **context):
        return self.walk(node.left, **context) + self.walk(node.right, **context)

    def walk__concat(self, node, **context):
        return str(self.walk(node.left, **context)) + str(self.walk(node.right, **context))

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
        return source.get_value(node.address, getattr(node, 'ws_name', ws_name))

    def walk__sum_function(self, node, **context):
        result = 0.0
        for operand in (self.walk(o, **context) for o in node.operands):
            try:
                result += sum(operand) if isinstance(operand, (list, Matrix)) else operand
            except TypeError:
                raise EFCValueError(operand)
        return result

    def walk__mod_function(self, node, **context):
        left_value, right_value = self.walk(node.left, **context), self.walk(node.right, **context)
        try:
            return left_value % right_value
        except TypeError:
            raise EFCValueError(left_value, right_value)

    def walk__iffunction(self, node, **context):
        return self.walk(node.true, **context) if self.walk(node.expr, **context) else self.walk(node.false, **context)

    def walk__iferrorfunction(self, node, **context):
        try:
            result = self.walk(node.expr, **context)
        except:
            result = self.walk(node.true, **context)
        return result

    def walk__max_function(self, node, **context):
        result = []
        for operand in (self.walk(o, **context) for o in node.operands):
            try:
                result.append(max(operand) if isinstance(operand, (list, Matrix)) else operand)
            except TypeError:
                raise EFCValueError(operand)
        return max(result)

    def walk__min_function(self, node, **context):
        result = []
        for operand in (self.walk(o, **context) for o in node.operands):
            try:
                result.append(min(operand) if isinstance(operand, (list, Matrix)) else operand)
            except TypeError:
                raise EFCValueError(operand)
        return min(result)

    def walk__left_function(self, node, **context):
        amount = self.walk(node.amount, **context)
        try:
            amount = int(amount)
        except ValueError:
            raise EFCValueError(amount)

        value = self.walk(node.expr, **context)
        try:
            value = str(value)
        except ValueError:
            raise EFCValueError(value)

        return value[:amount]

    def walk__right_function(self, node, **context):
        amount = self.walk(node.amount, **context)
        try:
            amount = int(amount)
        except ValueError:
            raise EFCValueError(amount)

        value = self.walk(node.expr, **context)
        try:
            value = str(value)
        except ValueError:
            raise EFCValueError(value)

        return value[-amount:]

    def walk__is_blank_function(self, node, **context):
        return self.walk(node.expr, **context) is None
