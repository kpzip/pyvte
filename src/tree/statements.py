from abc import ABC, abstractmethod

from context.context import ReturnValues
from context.context_stack import ContextStack
from tree.assignment_target import AssignmentTarget
from tree.expression import Expression


class Statement(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def execute(self, context_stack: ContextStack) -> bool:
        pass


class AssignmentStatement(Statement):

    def __init__(self, lhs: AssignmentTarget, rhs: Expression | None):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)


class AssertStatement(Statement):

    def __init__(self, expressions: list[Expression]):
        super().__init__()
        self.expressions = expressions

    def __str__(self):
        return "assert " + ", ".join(map(str, self.expressions))


class StatementList:

    def __init__(self, statents: list[Statement]):
        self.statements = statents

    def __str__(self):
        return "\n".join(map(str, self.statements))

    def execute(self, context_stack: ContextStack) -> bool:
        for s in self.statements:
            if s.execute(context_stack):
                return True
        return False


class SimpleStatementList(Statement):

    def __init__(self, statents: list[Statement]):
        super().__init__()
        self.statements = statents

    def __str__(self):
        return "; ".join(map(str, self.statements))

    def execute(self, context_stack: ContextStack) -> bool:
        for s in self.statements:
            if s.execute(ContextStack):
                return True
        return False


class IfStatement(Statement):

    def __init__(self, condition: Expression, code: StatementList):
        super().__init__()
        self.condition = condition
        self.code = code

    def __str__(self):
        return "if " + str(self.condition) + ":\n\t" + str(self.code).replace("\n", "\n\t")

    def execute(self, context_stack: ContextStack) -> bool:
        if self.condition.evaluate(context_stack).is_truthy():
            return self.code.execute(context_stack)
        return False


class ReturnStatement(Statement):

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr

    def __str__(self):
        return "return " + str(self.expr)

    def execute(self, context_stack: ContextStack) -> bool:
        context_stack.push(ReturnValues(self.expr.evaluate(context_stack)))
        return True
