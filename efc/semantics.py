# coding: utf8

from __future__ import unicode_literals, print_function
from tatsu.semantics import ModelBuilderSemantics
from efc.nodes import EFCBaseNode


def collect_class_descendants(base_class):
    subclasses = list(base_class.__subclasses__())
    descendants = set(subclasses)

    while subclasses:
        c = subclasses.pop()

        for subclass in (s for s in c.__subclasses__() if s not in descendants):
            descendants.add(subclass)
            subclasses.append(subclass)
    return descendants


class EFCModelBuilderSemantics(ModelBuilderSemantics):
    def __init__(self):
        super(EFCModelBuilderSemantics, self).__init__(base_type=EFCBaseNode,
                                                       types=collect_class_descendants(EFCBaseNode))
