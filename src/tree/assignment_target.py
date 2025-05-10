from abc import ABC

from tree.expression import Identifier


class AssignmentTarget(ABC):

    def __init__(self):
        pass


class SingleAssignmentTarget(AssignmentTarget):

    def __init__(self, target: Identifier):
        super().__init__()
        self.target = target

    def __str__(self):
        return str(self.target)
