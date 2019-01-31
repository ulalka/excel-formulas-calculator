# coding: utf8

from __future__ import unicode_literals, print_function
from efc.rpn.functions import EXCEL_FUNCTIONS
from efc.rpn.tokens import OperandToken, OperationToken, SingleCellToken, CellsRangeToken, NamedRangeToken
from efc.rpn.errors import OperandsMissing, FunctionNotSupported
from efc.rpn.operands import SimpleOperand, SingleCellOperand, CellRangeOperand, NamedRangeOperand

from six.moves import range


class Calculator(object):
    def calc(self, rpn, ws_name, source):
        result = []

        result_append = result.append
        result_pop = result.pop
        for token in rpn:
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
                                                source=source))
            elif isinstance(token, OperandToken):
                result_append(SimpleOperand(value=token.token_value,
                                            ws_name=ws_name,
                                            source=source))
            elif isinstance(token, OperationToken):
                try:
                    args = [result_pop() for _ in range(token.operands_count)]
                except IndexError:
                    raise OperandsMissing(token, rpn)

                args.reverse()

                try:
                    f = EXCEL_FUNCTIONS[token.src_value]
                except KeyError:
                    result_append(FunctionNotSupported())
                    continue

                v = f(*args)
                result_append(v)

        if len(result) == 1:
            return result[0].value if isinstance(result[0], SimpleOperand) else result[0]

        else:
            return result
