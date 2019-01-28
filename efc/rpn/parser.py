# coding: utf8

from __future__ import unicode_literals, print_function

from efc.rpn import tokens
from efc.rpn.tokens import (OperandToken, OperationToken, FunctionToken,
                            LeftBracketToken, RightBracketToken, Separator)
from efc.rpn.errors import InconsistentParentheses, SeparatorWithoutFunction

OPERATORS_PRIORITY = {
    tokens.ExponentToken: 4,
    tokens.MultiplyToken: 3,
    tokens.DivideToken: 3,
    tokens.SubtractToken: 2,
    tokens.CompareNotEqToken: 1,
    tokens.CompareGTEToken: 1,
    tokens.CompareLTEToken: 1,
    tokens.CompareGTToken: 1,
    tokens.CompareLTToken: 1,
    tokens.CompareEgToken: 1,
}


class Parser(object):
    @staticmethod
    def get_priority(token):
        return OPERATORS_PRIORITY.get(token.__class__, 0)

    def parse(self, line):
        get_priority = self.get_priority
        result = []
        stack = []
        operands_count = []

        result_append = result.append
        stack_append = stack.append
        stack_pop = stack.pop
        for token in line:
            if isinstance(token, OperandToken):
                result_append(token)
            elif isinstance(token, FunctionToken):
                stack_append(token)
            elif isinstance(token, LeftBracketToken):
                stack_append(token)
                operands_count.append(1)
            elif isinstance(token, OperationToken):
                priority = get_priority(token)
                while stack:
                    top_stack_token = stack[-1]
                    if (isinstance(top_stack_token, FunctionToken)
                            or get_priority(stack[-1]) >= priority):
                        result_append(stack_pop())
                    else:
                        break
                stack_append(token)
            elif isinstance(token, RightBracketToken):
                while stack:
                    top_stack_token = stack_pop()
                    if isinstance(top_stack_token, LeftBracketToken):
                        if stack:
                            t = stack[-1]
                            if isinstance(t, FunctionToken):
                                t.operands_count = operands_count.pop()
                        break
                    else:
                        result_append(top_stack_token)
                else:
                    raise InconsistentParentheses
            elif isinstance(token, Separator):
                if not operands_count:
                    raise SeparatorWithoutFunction
                operands_count[-1] += 1

        for stack_token in reversed(stack):
            if isinstance(stack_token, LeftBracketToken):
                raise InconsistentParentheses
            result_append(stack_token)

        return result
