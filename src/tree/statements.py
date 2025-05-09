from abc import ABC


class Statement(ABC):

    def __init__(self):
        pass


class AssignmentStatement(Statement):

    def __init__(self, lhs, rhs):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs


class StatementList:

    def __init__(self, statents: list[Statement]):
        self.statements = statents

    def __str__(self):
        return "\n".join(self.statements)
