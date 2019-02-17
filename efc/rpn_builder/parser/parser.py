# coding: utf8

from __future__ import unicode_literals, print_function

from efc.rpn_builder.lexer.tokens import (OperandToken, OperationToken, FunctionToken, LeftBracketToken,
                                          RightBracketToken,
                                          Separator, SubtractToken, ArithmeticToken, AddToken, ExponentToken,
                                          MultiplyToken,
                                          DivideToken, ConcatToken, SingleCellToken, CellsRangeToken, NamedRangeToken)
from efc.rpn_builder.errors import InconsistentParentheses, SeparatorWithoutFunction
from efc.rpn_builder.parser.operands import SingleCellOperand, NamedRangeOperand, CellRangeOperand, SimpleOperand
from efc.rpn_builder.rpn import RPN
from efc.rpn_builder.parser.operations import Operation, ArithmeticOperation, FunctionOperation

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

    def operand_token_handler(self, token, ws_name, source):
        if isinstance(token, SingleCellToken):
            return SingleCellOperand(row=token.row, column=token.column,
                                     ws_name=token.ws_name or ws_name,
                                     source=source)
        elif isinstance(token, CellsRangeToken):
            return CellRangeOperand(row1=token.row1, column1=token.column1,
                                    row2=token.row2, column2=token.column2,
                                    ws_name=token.ws_name or ws_name,
                                    source=source)
        elif isinstance(token, NamedRangeToken):
            return NamedRangeOperand(name=token.name,
                                     ws_name=token.ws_name or ws_name,
                                     source=source).value
        else:
            return SimpleOperand(value=token.token_value,
                                 ws_name=ws_name,
                                 source=source)

    def operation_token_handler(self, line):
        current_token = line.current()
        prev_token = line.prev()
        operation = ArithmeticOperation(current_token.src_value, self.get_priority(current_token))
        if (isinstance(current_token, (SubtractToken, AddToken)) and (
                isinstance(prev_token, (ArithmeticToken, LeftBracketToken, Separator)) or prev_token is None)):
            operation.operands_count = 1
        return operation

    def to_rpn(self, line, ws_name, source):
        result = RPN()
        stack = []

        result_append = result.append
        stack_append = stack.append
        stack_pop = stack.pop
        while not line.is_ended:
            token = next(line)
            if isinstance(token, OperandToken):
                result_append(self.operand_token_handler(token, ws_name, source))
            elif isinstance(token, FunctionToken):
                stack_append(FunctionOperation(token.src_value))
            elif isinstance(token, LeftBracketToken):
                stack_append(token)
            elif isinstance(token, OperationToken):
                operation = self.operation_token_handler(line)
                while stack:
                    if isinstance(stack[-1], Operation) and stack[-1].priority >= operation.priority:
                        result_append(stack_pop())
                    else:
                        break
                stack_append(operation)
            elif isinstance(token, RightBracketToken):
                while stack:
                    top_stack_token = stack_pop()
                    if isinstance(top_stack_token, LeftBracketToken):
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

                if len(stack) > 1 and isinstance(stack[-2], FunctionOperation):
                    stack[-2].operands_count += 1

        for stack_token in reversed(stack):
            if isinstance(stack_token, LeftBracketToken):
                raise InconsistentParentheses
            result_append(stack_token)

        return result
