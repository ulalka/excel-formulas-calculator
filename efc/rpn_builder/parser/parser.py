# coding: utf8

from __future__ import unicode_literals, print_function

from efc.rpn_builder.lexer.tokens import (OperandToken, OperationToken, FunctionToken, LeftBracketToken, RightBracketToken,
                                          Separator, SubtractToken, ArithmeticToken, AddToken, ExponentToken, MultiplyToken,
                                          DivideToken, ConcatToken, SingleCellToken, CellsRangeToken, NamedRangeToken)
from efc.rpn_builder.errors import InconsistentParentheses, SeparatorWithoutFunction
from efc.rpn_builder.parser.operands import SingleCellOperand, NamedRangeOperand, CellRangeOperand, SimpleOperand
from efc.rpn_builder.rpn import RPN

__all__ = ('Parser',)

OPERATORS_PRIORITY = {
    ExponentToken: 5,
    MultiplyToken: 4,
    DivideToken: 4,
    SubtractToken: 3,
    AddToken: 2,
    ConcatToken: 1,
}


class Parser(object):
    @staticmethod
    def get_priority(token):
        return OPERATORS_PRIORITY.get(token.__class__, 0)

    def to_rpn(self, line, ws_name, source):
        get_priority = self.get_priority
        result = RPN()
        stack = []
        operands_count = []

        result_append = result.append
        stack_append = stack.append
        stack_pop = stack.pop
        prev_token = None
        for token in line:
            if isinstance(token, SingleCellToken):
                result_append(SingleCellOperand(row=token.row, column=token.column,
                                                ws_name=token.ws_name or ws_name,
                                                source=source))
            elif isinstance(token, CellsRangeToken):
                result_append(CellRangeOperand(row1=token.row1, column1=token.column1,
                                               row2=token.row2, column2=token.column2,
                                               ws_name=token.ws_name or ws_name,
                                               source=source))
            elif isinstance(token, NamedRangeToken):
                result_append(NamedRangeOperand(name=token.name,
                                                ws_name=token.ws_name or ws_name,
                                                source=source).value)
            elif isinstance(token, OperandToken):
                result_append(SimpleOperand(value=token.token_value,
                                            ws_name=ws_name,
                                            source=source))
            elif isinstance(token, FunctionToken):
                stack_append(token)
            elif isinstance(token, LeftBracketToken):
                if isinstance(prev_token, FunctionToken):
                    operands_count.append(1)
                stack_append(token)
            elif isinstance(token, OperationToken):
                if (isinstance(token, (SubtractToken, AddToken)) and
                        (isinstance(prev_token, (ArithmeticToken, LeftBracketToken, Separator))
                         or prev_token is None)):
                    token.operands_count = 1

                priority = get_priority(token)
                while stack:
                    top_stack_token = stack[-1]
                    if (isinstance(top_stack_token, FunctionToken)
                            or isinstance(top_stack_token, OperationToken)
                            and get_priority(top_stack_token) >= priority):
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
                try:
                    while not isinstance(stack[-1], LeftBracketToken):
                        result_append(stack_pop())
                except IndexError:
                    raise SeparatorWithoutFunction

                if len(stack) > 1 and isinstance(stack[-2], FunctionToken):
                    operands_count[-1] += 1
            prev_token = token

        for stack_token in reversed(stack):
            if isinstance(stack_token, LeftBracketToken):
                raise InconsistentParentheses
            result_append(stack_token)

        return result
