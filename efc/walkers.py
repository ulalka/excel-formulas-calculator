# coding: utf8
from __future__ import unicode_literals

from tatsu.objectmodel import Node
from tatsu.semantics import ModelBuilderSemantics


class CalcModelBuilderSemantics(ModelBuilderSemantics):
    def __init__(self):
        types = [
            t for t in globals().values()
            if type(t) is type and issubclass(t, ModelBase)
        ]
        super(CalcModelBuilderSemantics, self).__init__(types=types)


class ModelBase(Node):
    pass


class Add(ModelBase):
    def __init__(self,
                 left=None,
                 op=None,
                 right=None,
                 **kwargs):
        super(Add, self).__init__(
            left=left,
            op=op,
            right=right,
            **kwargs
        )


# FIXME 1 - 1 - 1 = 1, should change op priority
class Subtract(ModelBase):
    def __init__(self,
                 left=None,
                 op=None,
                 right=None,
                 **kwargs):
        super(Subtract, self).__init__(
            left=left,
            op=op,
            right=right,
            **kwargs
        )


class Multiply(ModelBase):
    def __init__(self,
                 left=None,
                 op=None,
                 right=None,
                 **kwargs):
        super(Multiply, self).__init__(
            left=left,
            op=op,
            right=right,
            **kwargs
        )


class Divide(ModelBase):
    def __init__(self,
                 left=None,
                 right=None,
                 **kwargs):
        super(Divide, self).__init__(
            left=left,
            right=right,
            **kwargs
        )


class Exponent(ModelBase):
    def __init__(self,
                 left=None,
                 right=None,
                 **kwargs):
        super(Exponent, self).__init__(
            left=left,
            right=right,
            **kwargs
        )


class ConcatString(ModelBase):
    def __init__(self, left=None, right=None, **kwargs):
        super(ConcatString, self).__init__(left=left, right=right, **kwargs)


class CompareBase(ModelBase):
    pass


class CompareEq(CompareBase):
    def __init__(self, left=None, right=None, **kwargs):
        super(CompareEq, self).__init__(left=left, right=right, **kwargs)
